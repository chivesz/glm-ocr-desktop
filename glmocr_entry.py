import os
import sys

if getattr(sys, "frozen", False):
    # PyInstaller 6.x stores data files in _internal/ (sys._MEIPASS)
    _internal_dir = sys._MEIPASS
    _models_dir = os.path.join(_internal_dir, "models")

    # PP-DocLayoutV3 is small and always bundled — force offline so it never
    # tries to reach HuggingFace Hub.
    _layout_model = os.path.join(_models_dir, "PP-DocLayoutV3")
    if os.path.isdir(_layout_model):
        os.environ.setdefault("GLMOCR_LAYOUT_MODEL_DIR", _layout_model)
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"

    # GLM-OCR is too large to ship in the release zip.
    # Check bundled path first; fall back to %APPDATA%\glmocr\models\GLM-OCR
    # so the app can auto-download on first run.
    _glm_bundled = os.path.join(_models_dir, "GLM-OCR")
    _glm_user = os.path.join(
        os.environ.get("APPDATA") or os.path.expanduser("~"),
        "glmocr", "models", "GLM-OCR",
    )
    _glm_model = _glm_bundled if os.path.isdir(_glm_bundled) else _glm_user
    os.environ.setdefault("GLMOCR_LOCAL_OCR_MODEL", _glm_model)
    if os.path.isdir(_glm_bundled):
        # Both models are local — stay fully offline.
        pass
    else:
        # Allow HuggingFace downloads so the model can be fetched on first run.
        os.environ.pop("HF_HUB_OFFLINE", None)
        os.environ.pop("TRANSFORMERS_OFFLINE", None)

from glmocr.cli import main

if __name__ == "__main__":
    main()
