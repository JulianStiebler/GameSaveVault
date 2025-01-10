# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../../main.py'],  # The main Python script
    pathex=[],  # Additional paths if needed
    binaries=[],  # Include binaries if needed
    datas=[],  # Include any additional data files
    hiddenimports=[],  # Hidden imports, if any
    hookspath=[],  # Hook paths, if any
    hooksconfig={},  # Hook configuration, if any
    runtime_hooks=[],  # Runtime hooks, if any
    excludes=[],  # Exclude modules you don't want to bundle
    noarchive=False,  # Don't bundle into a single archive
    optimize=0,  # Level of optimization (0: no optimization)
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GameSaveVault',  # output executable name
    debug=False,  # Set to True if you want debugging symbols
    bootloader_ignore_signals=False,  # Ignore signals from bootloader
    strip=False,  # Don't strip symbols (helps in debugging)
    upx=True,  # Compress executable with UPX
    upx_exclude=[],  # Exclude files from UPX compression
    runtime_tmpdir=None,  # Runtime temp directory (optional)
    console=False,  # Set to False to hide console window (for GUI apps)
    disable_windowed_traceback=False,  # Set to True to disable traceback in windowed mode
    argv_emulation=False,  # Set to True to emulate command-line arguments
    target_arch=None,  # Architecture (optional, for cross-compilation)
    codesign_identity=None,  # Optional: for signing executables on macOS
    entitlements_file=None,  # Optional: for entitlements (macOS)
)
