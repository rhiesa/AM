@echo off
echo Setting up Risk Assessment Tool...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.7+ from https://python.org
    echo Then run this script again.
    pause
    exit /b 1
)

echo Installing required packages...
python -m pip install --user -r requirements.txt

if %errorlevel% neq 0 (
    echo Error installing packages. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo You can now run the application using run.bat
echo.
pause
