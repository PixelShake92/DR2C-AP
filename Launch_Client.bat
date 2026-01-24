@echo off
cd /d "%~dp0"

if exist "DRTC_Client.py" (
    set "CLIENT=DRTC_Client.py"
) else if exist "DRTC_Client.pyw" (
    set "CLIENT=DRTC_Client.pyw"
) else (
    echo ERROR: DRTC_Client.py not found in this folder!
    pause
    exit /b
)

start "DRTC Client" python %CLIENT%
timeout /t 2 /nobreak >nul
start "" steam://rungameid/252610
