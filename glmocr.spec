# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import (
    collect_all,
    collect_data_files,
    collect_dynamic_libs,
    collect_submodules,
)

block_cipher = None

# Collect full packages for heavy ML deps
torch_datas, torch_binaries, torch_hiddenimports = collect_all('torch')
torchvision_datas, torchvision_binaries, torchvision_hiddenimports = collect_all('torchvision')
transformers_datas, transformers_binaries, transformers_hiddenimports = collect_all('transformers')
cv2_datas, cv2_binaries, cv2_hiddenimports = collect_all('cv2')
tokenizers_datas, tokenizers_binaries, tokenizers_hiddenimports = collect_all('tokenizers')
sentencepiece_datas, sentencepiece_binaries, sentencepiece_hiddenimports = collect_all('sentencepiece')
accelerate_datas, accelerate_binaries, accelerate_hiddenimports = collect_all('accelerate')
safetensors_datas, safetensors_binaries, safetensors_hiddenimports = collect_all('safetensors')
pypdfium2_datas, pypdfium2_binaries, pypdfium2_hiddenimports = collect_all('pypdfium2')

pymupdf_datas = collect_data_files('pymupdf')
pymupdf_binaries = collect_dynamic_libs('pymupdf')

glmocr_datas = [
    ('glmocr/config.yaml', 'glmocr'),
]
if os.path.isdir('models/PP-DocLayoutV3'):
    glmocr_datas.append(('models/PP-DocLayoutV3', 'models/PP-DocLayoutV3'))
if os.path.isdir('models/GLM-OCR'):
    glmocr_datas.append(('models/GLM-OCR', 'models/GLM-OCR'))

all_datas = (
    torch_datas
    + torchvision_datas
    + transformers_datas
    + cv2_datas
    + tokenizers_datas
    + sentencepiece_datas
    + accelerate_datas
    + safetensors_datas
    + pypdfium2_datas
    + pymupdf_datas
    + glmocr_datas
)

all_binaries = (
    torch_binaries
    + torchvision_binaries
    + transformers_binaries
    + cv2_binaries
    + tokenizers_binaries
    + sentencepiece_binaries
    + accelerate_binaries
    + safetensors_binaries
    + pypdfium2_binaries
    + pymupdf_binaries
)

all_hiddenimports = (
    torch_hiddenimports
    + torchvision_hiddenimports
    + transformers_hiddenimports
    + cv2_hiddenimports
    + tokenizers_hiddenimports
    + sentencepiece_hiddenimports
    + accelerate_hiddenimports
    + safetensors_hiddenimports
    + pypdfium2_hiddenimports
    + [
        'glmocr',
        'glmocr.cli',
        'glmocr.api',
        'glmocr.config',
        'glmocr.local_ocr_client',
        'glmocr.maas_client',
        'glmocr.parser_result',
        'glmocr.pipeline',
        'glmocr.pipeline.pipeline',
        'glmocr.utils',
        'glmocr.utils.logging',
        'glmocr.utils.markdown_utils',
        'torch._C',
        'torch._C._VariableFunctions',
        'torch.nn',
        'torch.nn.functional',
        'torch.nn.modules',
        'torch.nn.modules.activation',
        'torch.nn.modules.batchnorm',
        'torch.nn.modules.container',
        'torch.nn.modules.conv',
        'torch.nn.modules.linear',
        'torch.nn.modules.loss',
        'torch.nn.modules.normalization',
        'torch.nn.modules.pooling',
        'torch.nn.modules.transformer',
        'torch.nn.parallel',
        'torch.autograd',
        'torch.optim',
        'torch.cuda',
        'torch.distributed',
        'torch.jit',
        'torch.utils',
        'torch.utils.data',
        'torch.backends',
        'torch.backends.cpu',
        'torch.backends.cudnn',
        'torch.ops',
        'torchvision.transforms',
        'torchvision.transforms.functional',
        'torchvision.models',
        'transformers.modeling_utils',
        'transformers.tokenization_utils',
        'transformers.configuration_utils',
        'transformers.models.auto',
        'transformers.image_processing_utils',
        'pydantic',
        'pydantic.v1',
        'pydantic_core',
        'yaml',
        'dotenv',
        'portalocker',
        'portalocker.utils',
        'portalocker.exceptions',
        'portalocker.portalocker',
        'tqdm',
        'tqdm.auto',
        'tqdm.utils',
        'requests',
        'requests.adapters',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'PIL',
        'PIL.Image',
        'numpy',
        'pymupdf',
        'fitz',
        'colorama',
        'packaging',
        'annotated_types',
        'typing_extensions',
        'typing_inspection',
        'huggingface_hub',
        'huggingface_hub.utils',
        'filelock',
        'fsspec',
        'sympy',
        'networkx',
        'regex',
        'psutil',
        'unittest',
        'unittest.case',
        'unittest.mock',
        'unittest.util',
        'unittest.loader',
        'unittest.suite',
        'unittest.runner',
        'unittest.signals',
        'unittest.result',
    ]
)

a = Analysis(
    ['glmocr_entry.py'],
    pathex=[os.path.abspath('.')],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    excludes=[
        'torchaudio',
        'sklearn',
        'scipy',
        'matplotlib',
        'tensorflow',
        'keras',
        'flash_attn',
        'triton',
        'vllm',
        'flask',
        'fastapi',
        'uvicorn',
        'tkinter',
        '_tkinter',
        'IPython',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='glmocr',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='glmocr',
)
