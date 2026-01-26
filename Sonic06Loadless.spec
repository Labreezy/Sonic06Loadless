# -*- mode: python ; coding: utf-8 -*-
"""
Sonic06Loadless.spec

Produces three standalone one-file executables in ./dist/:
 - sa1_loadless  -> main_sa1.py
 - 06_loadless   -> main_06.py
 - 06_retime     -> retime_06.py

Run `pyinstaller Sonic06Loadless.spec` on each target OS to produce native binaries.
"""

import os
import shutil
import sys

block_cipher = None

# auto-detect UPX on PATH
_upx_available = shutil.which("upx") is not None

# make relative imports/resources work
pathex = [os.path.abspath('.')]

# ---------------- Entry: main_sa1.py -> sa1_loadless ----------------
a_sa1 = Analysis(
    ['main_sa1.py'],
    pathex=pathex,
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz_sa1 = PYZ(a_sa1.pure, a_sa1.zipped_data, cipher=block_cipher)

exe_sa1 = EXE(
    pyz_sa1,
    a_sa1.scripts,
    a_sa1.binaries,
    a_sa1.zipfiles,
    a_sa1.datas,
    [],
    name='sa1_loadless',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=_upx_available,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ---------------- Entry: main_06.py -> 06_loadless ----------------
a_06 = Analysis(
    ['main_06.py'],
    pathex=pathex,
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz_06 = PYZ(a_06.pure, a_06.zipped_data, cipher=block_cipher)

exe_06 = EXE(
    pyz_06,
    a_06.scripts,
    a_06.binaries,
    a_06.zipfiles,
    a_06.datas,
    [],
    name='06_loadless',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=_upx_available,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ---------------- Entry: retime_06.py -> 06_retime ----------------
a_retime = Analysis(
    ['retime_06.py'],
    pathex=pathex,
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz_retime = PYZ(a_retime.pure, a_retime.zipped_data, cipher=block_cipher)

exe_retime = EXE(
    pyz_retime,
    a_retime.scripts,
    a_retime.binaries,
    a_retime.zipfiles,
    a_retime.datas,
    [],
    name='06_retime',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=_upx_available,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
