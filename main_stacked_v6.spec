# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_stacked_v6.py'],
    pathex=['C:\\Users\\benst\\Documents\\Workspace\\DXR'],
    binaries=[],
    datas=[('C:\\Users\\benst\\Documents\\Workspace\\DXR\\assets\\projnet.png', '.'), ('C:\\Users\\benst\\Documents\\Workspace\\DXR\\assets\\drx_review.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='DXR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\benst\\Documents\\Workspace\\DXR\\assets\\icon.ico'],
)
