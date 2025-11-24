@echo off
REM BackupWin - English Version Launcher
REM This sets English language preference and launches the application

echo {"language": "en"} > .language_config.json
call run_gui.bat
