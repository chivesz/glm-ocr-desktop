# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

pymupdf_datas = collect_data_files('pymupdf')
pymupdf_binaries = collect_dynamic_libs('pymupdf')
glmocr_datas = [('glmocr/config.yaml', 'glmocr')]

a = Analysis(
    ['glmocr_entry.py'],
    pathex=[os.path.abspath('.')],
    binaries=pymupdf_binaries,
    datas=pymupdf_datas + glmocr_datas,
    hiddenimports=[
        'glmocr',
        'glmocr.cli',
        'glmocr.api',
        'glmocr.config',
        'glmocr.maas_client',
        'glmocr.parser_result',
        'glmocr.utils',
        'glmocr.utils.logging',
        'glmocr.utils.markdown_utils',
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
    ],
    excludes=[
        'torch',
        'torchvision',
        'torchaudio',
        'transformers',
        'accelerate',
        'sentencepiece',
        'cv2',
        'opencv',
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
        'test',
        'unittest',
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
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='glmocr',
)
