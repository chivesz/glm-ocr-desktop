import os
import sys

if getattr(sys, "frozen", False):
    # PyInstaller 6.x stores data files in _internal/ (sys._MEIPASS)
    _internal_dir = sys._MEIPASS
    _models_dir = os.path.join(_internal_dir, "models")
    # Prevent any runtime downloads from HuggingFace Hub
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    # Point layout detector at bundled PP-DocLayoutV3 model
    os.environ.setdefault("GLMOCR_LAYOUT_MODEL_DIR", os.path.join(_models_dir, "PP-DocLayoutV3"))
    # Point OCR inference at bundled GLM-OCR model
    os.environ.setdefault("GLMOCR_LOCAL_OCR_MODEL", os.path.join(_models_dir, "GLM-OCR"))

from glmocr.cli import main

if __name__ == "__main__":
    main()
