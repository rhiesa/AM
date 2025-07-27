@echo off
echo Starting Risk Assessment Tool...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH. Using portable Python...
    if exist "python\python.exe" (
        python\python.exe app\gui.py
    ) else (
        echo Error: Python not found. Please install Python 3.7+ or use the portable version.
        pause
        exit /b 1
    )
) else (
    echo Using system Python...
    python app\gui.py
)

if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error.
    pause
)
