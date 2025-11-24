@echo off
REM BackupWin - Vietnamese Version Launcher
REM This sets Vietnamese language preference and launches the application

echo {"language": "vi"} > .language_config.json
call run_gui.bat
