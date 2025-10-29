# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['dxr.py'],
    pathex=['C:\\Users\\j2ee9bsf\\Documents\\00 Workspace\\DXR'],
    binaries=[],
    datas=[('C:\\Users\\j2ee9bsf\\Documents\\00 Workspace\\DXR\\assets', '.\\assets'), ('C:\\Users\\j2ee9bsf\\Documents\\00 Workspace\\DXR\\dxgui', '.\\dxgui')],
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
    codesign_identity='Developer ID Application: Ben Fisher (4d2771dfc6504e1fad77441da50391c3)',
    entitlements_file=None,
    icon=['C:\\Users\\j2ee9bsf\\Documents\\00 Workspace\\DXR\\assets\\icon.ico'],
)
