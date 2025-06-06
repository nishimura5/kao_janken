@echo off
setlocal

echo [1/3] Installing uv...
powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"

set CARGO_BIN=%USERPROFILE%\.cargo\bin

echo [2/3] Adding %CARGO_BIN% to PATH...

:: Add to user environment variable PATH if not already present
for /f "tokens=*" %%i in ('reg query HKCU\Environment /v Path 2^>nul') do set CUR_PATH=%%i

echo %CUR_PATH% | find /i "%CARGO_BIN%" >nul
if errorlevel 1 (
    setx Path "%CARGO_BIN%;%Path%"
    echo Added: %CARGO_BIN%
) else (
    echo Already present in PATH.
)

echo [3/3] Done. Please restart your terminal.
endlocal
pause
