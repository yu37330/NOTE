# -*- mode: python ; coding: utf-8 -*-

import site
import os

block_cipher = None

assert len(site.getsitepackages()) > 0

package_path = site.getsitepackages()[0]
for p in site.getsitepackages():
    if "site-package" in p:
        package_path = p
        break

a = Analysis(
     ['ANOMALY_streamlit.py'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join(package_path, "altair/vegalite/v5/schema/vega-lite-schema.json"), "./altair/vegalite/v5/schema/"),
        (os.path.join(package_path, "streamlit/static"), "./streamlit/static"),
        (os.path.join(package_path, "streamlit/runtime"), "./streamlit/runtime")
    ],
    hiddenimports=[
        'streamlit', 'importlib_metadata', 'importlib_resources', 
        'streamlit.web.server', 'streamlit.runtime.scriptrunner',
        'seaborn', 'scipy.optimize.curve_fit'
    ],
    hookspath=['./hooks'],
    runtime_hooks=[],
    excludes=[],
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
    name='ANOMALY_streamlit',
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
)
