# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for BackupWin"""

block_cipher = None

a = Analysis(
    ['gui_app_i18n.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('Cai dat phan mem', 'Cai dat phan mem'),
        ('OFFICE, WINRAR, IDM', 'OFFICE, WINRAR, IDM'),
        ('Sao luu du lieu', 'Sao luu du lieu'),
    ],
    hiddenimports=[
        # GUI
        'customtkinter',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        # Pydantic
        'pydantic',
        'pydantic_settings',
        'pydantic.deprecated.decorator',
        'pydantic_core',
        'pydantic.fields',
        'pydantic.main',
        # Logging
        'loguru',
        # App modules
        'app.services.file_search',
        'app.services.backup',
        'app.services.file_consolidation',
        'app.services.duplicate_finder',
        'app.core.config',
        'app.core.logger',
        # GUI modules
        'gui.search_tab_i18n',
        'gui.backup_tab_i18n',
        'gui.restore_tab_i18n',
        'gui.consolidate_tab_i18n',
        'gui.duplicate_finder_tab_i18n',
        'gui.organizer_tab_i18n',
        'gui.resources_tab_i18n',
        'gui.components',
        'gui.styles',
        'gui.i18n',
        'gui.tab_header',
        'gui.locales.en',
        'gui.locales.vi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2',
        'alembic',
        'httpx',
        'boto3',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BackupWin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file here if you have one
)
