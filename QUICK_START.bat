@echo off
color 0A
echo.
echo     ========================================
echo          BackupWin - Quick Start
echo     ========================================
echo.
echo     Choose an option:
echo.
echo     1. Run GUI (Auto-detect language)
echo     2. Run GUI (English)
echo     3. Run GUI (Vietnamese / Tieng Viet)
echo     4. Install GUI and Run (First Time)
echo     5. Build Standalone Executable
echo     6. Test Dependencies
echo     7. Exit
echo.
echo     ========================================
echo.

choice /c 1234567 /n /m "     Enter your choice (1-7): "

if errorlevel 7 goto :exit
if errorlevel 6 goto :test
if errorlevel 5 goto :build
if errorlevel 4 goto :install
if errorlevel 3 goto :runvi
if errorlevel 2 goto :runen
if errorlevel 1 goto :run

:run
echo.
echo Starting BackupWin GUI...
call run_gui.bat
goto :exit

:runen
echo.
echo Starting BackupWin GUI (English)...
call run_gui_english.bat
goto :exit

:install
echo.
echo Installing dependencies...
call install_gui_deps.bat
if errorlevel 1 (
    echo Installation failed!
    pause
    exit /b 1
)
echo.
echo Installation complete! Starting application...
timeout /t 2 /nobreak >nul
call run_gui.bat
goto :exit

:runvi
echo.
echo Starting BackupWin GUI (Vietnamese)...
call run_gui_vietnamese.bat
goto :exit

:build
echo.
echo Building executable...
call build_exe.bat
goto :exit

:test
echo.
echo Testing dependencies...
call test_dependencies.bat
goto :exit

:exit
exit
