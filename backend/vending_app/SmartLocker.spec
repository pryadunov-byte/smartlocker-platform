# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller specification for the SmartLocker application."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

project_dir = Path(__file__).resolve().parent
import sys

if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))
pathex = [str(project_dir)]

package_names = ("gui", "serial", "services", "db")
datas = [(str(project_dir / "config.json"), ".")]
hiddenimports: list[str] = []

for package in package_names:
    datas.extend(collect_data_files(package))
    hiddenimports.extend(collect_submodules(package))

unique_datas = []
seen = set()
for entry in datas:
    if tuple(entry) not in seen:
        unique_datas.append(entry)
        seen.add(tuple(entry))
datas = unique_datas
hiddenimports = sorted(set(hiddenimports))

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=pathex,
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SmartLocker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
