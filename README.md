# glm-ocr-desktop

Offline desktop OCR tool for receipts, invoices, and documents. No internet connection required, no API key, no external server — everything runs locally on your machine.

Built on [GLM-OCR](https://github.com/zai-org/GLM-OCR) (Zhipu AI) and [PP-DocLayoutV3](https://huggingface.co/PaddlePaddle/PP-DocLayoutV3_safetensors) (PaddlePaddle).

---

## What it does

- Takes a photo or scan of a receipt, invoice, or document
- Detects layout regions (text blocks, tables, formulas)
- Runs OCR on each region using a local 0.9B vision-language model
- Outputs structured Markdown and JSON — ready to feed into accounting or other software

## Download

Download the latest release from the [Releases](../../releases) page.  
Unzip and run — no installation needed.

## Usage

```
glmocr.exe parse receipt.jpg
glmocr.exe parse invoice.pdf --output C:\results
glmocr.exe parse C:\scans\ --output C:\results
```

Output files per document:
- `.md` — extracted text, tables, and formulas as Markdown
- `.json` — structured regions with bounding boxes and content
- `layout_vis/` — visualization of detected regions

## Build from source

**Requirements:** Python 3.12, [uv](https://github.com/astral-sh/uv)

```bash
git clone https://github.com/chivesz/glm-ocr-desktop.git
cd glm-ocr-desktop

uv venv .venv --python 3.12
.venv\Scripts\activate

# Install CPU-only torch (swap for CUDA build if you have a GPU)
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
uv pip install -e ".[selfhosted]"
uv pip install pyinstaller

# Download models (~2.6 GB)
python scripts/download_models.py

# Build the binary
pyinstaller glmocr.spec --distpath dist_build
```

Binary will be at `dist_build\glmocr\glmocr.exe`.

## License

This project uses components under MIT and Apache 2.0 licenses. Commercial use is permitted. See [LICENSES/](LICENSES/) for full texts.
