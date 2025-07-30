# -*- mode: python ; coding: utf-8 -*-

# RAGFlow Client PyInstaller 配置文件

import sys
import os

# 添加当前目录到路径
block_cipher = None

# 分析主程序
a = Analysis(
    ['ragflow_client.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.json.example', '.'),
        ('test_data', 'test_data'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'requests',
        'json',
        'logging',
        'pathlib',
        'typing',
        'argparse',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 打包程序
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 创建可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ragflow-client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)