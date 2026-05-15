"""Download GLM-OCR and PP-DocLayoutV3 models for offline bundling."""
import os
from pathlib import Path
from huggingface_hub import snapshot_download

root = Path(__file__).parent.parent / "models"
root.mkdir(exist_ok=True)

print("Downloading PP-DocLayoutV3 layout model …")
snapshot_download(
    "PaddlePaddle/PP-DocLayoutV3_safetensors",
    local_dir=str(root / "PP-DocLayoutV3"),
    ignore_patterns=["*.msgpack", "*.h5", "flax_model*", "tf_model*", "rust_model*"],
)
print("PP-DocLayoutV3 done.")

print("Downloading GLM-OCR model …")
snapshot_download(
    "zai-org/GLM-OCR",
    local_dir=str(root / "GLM-OCR"),
    ignore_patterns=["*.msgpack", "*.h5", "flax_model*", "tf_model*", "rust_model*", "original/*"],
)
print("GLM-OCR done.")
print("All models downloaded to", root)
