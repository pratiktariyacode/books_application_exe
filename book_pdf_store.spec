# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('users.db', '.'),                     # DB File
        ('ui/book5.png', 'ui'),                    # Any standalone book image
        ('ui/icon.ico', 'ui'),                 # App icon
        ('ui/book1.jpg', 'ui'),                # Background Image
        ('ui/*.png', 'ui'),                    # Extra images (if any)
        ('assets/images', 'assets/images'),    # All book images (if stored separately)
        ('assets/pdf', 'assets/pdf'),          # All PDFs
        ('ui/book3.webp', 'ui'),  
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='book_pdf_store',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you want to see errors in console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ui/icon.ico',  # Windows icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='book_pdf_store',
)
