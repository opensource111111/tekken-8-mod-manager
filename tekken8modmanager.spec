# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tekken8modmanager.py'],
    pathex=[],
    binaries=[('dep/glfw-3.4.bin.WIN64/lib-mingw-w64/glfw3.dll', '.'),('dep/glfw-3.4.bin.WIN64/lib-mingw-w64/libglfw3.a', ',')],
    datas=[('assets/icon.ico', '.'), ('assets/arial.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='tekken8modmanager',
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
    icon=['assets\\icon.ico'],
)
