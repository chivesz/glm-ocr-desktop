from __future__ import annotations

import base64
import io
import os
from typing import Dict, Tuple, Optional

from glmocr.utils.logging import get_logger

logger = get_logger(__name__)


class LocalOCRClient:
    """Run GLM-OCR inference in-process via transformers (no external server)."""

    def __init__(self, model_path: str):
        self._model_path = model_path
        self._model = None
        self._processor = None

    def start(self):
        import torch
        from transformers import AutoProcessor, AutoModelForImageTextToText

        logger.info("Loading GLM-OCR model from %s …", self._model_path)
        self._processor = AutoProcessor.from_pretrained(
            self._model_path, local_files_only=True
        )
        dtype = torch.float32 if not torch.cuda.is_available() else torch.bfloat16
        self._model = AutoModelForImageTextToText.from_pretrained(
            self._model_path,
            torch_dtype=dtype,
            device_map="auto",
            local_files_only=True,
        )
        self._model.eval()
        logger.info("GLM-OCR model loaded on %s", next(self._model.parameters()).device)

    def stop(self):
        self._model = None
        self._processor = None

    def is_alive(self, timeout: float = 5.0) -> bool:
        return self._model is not None

    def process(self, request_data: Dict) -> Tuple[Dict, int]:
        if self._model is None or self._processor is None:
            return {"error": "LocalOCRClient not started"}, 500

        messages = request_data.get("messages", [])
        max_tokens = int(request_data.get("max_tokens", 8192))

        user_msg = next((m for m in messages if m.get("role") == "user"), None)
        if not user_msg:
            return {"error": "No user message in request"}, 400

        text_prompt = "Text Recognition:"
        pil_image = None

        from PIL import Image

        for item in user_msg.get("content", []):
            if item.get("type") == "text":
                text_prompt = item.get("text", text_prompt)
            elif item.get("type") == "image_url":
                url = item.get("image_url", "")
                if isinstance(url, dict):
                    url = url.get("url", "")
                if url.startswith("data:"):
                    _, b64 = url.split(",", 1)
                    pil_image = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")

        if pil_image is None:
            return {"error": "No image found in request"}, 400

        chat_messages = [{"role": "user", "content": [
            {"type": "image"},
            {"type": "text", "text": text_prompt},
        ]}]

        try:
            import torch
            inputs = self._processor.apply_chat_template(
                chat_messages,
                images=[pil_image],
                tokenize=True,
                add_generation_prompt=True,
                return_dict=True,
                return_tensors="pt",
            ).to(next(self._model.parameters()).device)
            inputs.pop("token_type_ids", None)

            with torch.no_grad():
                generated_ids = self._model.generate(**inputs, max_new_tokens=max_tokens)

            output = self._processor.decode(
                generated_ids[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=False,
            )
            return {"choices": [{"message": {"content": output.strip()}}]}, 200

        except Exception as e:
            logger.error("Local inference error: %s", e)
            return {"error": str(e)}, 500
