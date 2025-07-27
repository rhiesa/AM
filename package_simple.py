#!/usr/bin/env python3
"""
Simple packaging script for Risk Assessment Tool
Creates a portable Python environment with all dependencies
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path

def create_portable_package():
    """Create a portable package with Python and all dependencies"""
    print("=== Creating Portable Risk Assessment Tool Package ===")
    print()
    
    # Create package directory
    package_dir = "RiskAssessmentTool_Portable"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Create subdirectories
    os.makedirs(os.path.join(package_dir, "python"))
    os.makedirs(os.path.join(package_dir, "app"))
    os.makedirs(os.path.join(package_dir, "data"))
    
    print("Created package directory structure")
    
    # Copy application files
    app_files = ["gui.py", "risk_assessment.py"]
    for file in app_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(package_dir, "app"))
            print(f"Copied {file}")
    
    # Create launcher script
    launcher_content = '''@echo off
echo Starting Risk Assessment Tool...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH. Using portable Python...
    if exist "python\\python.exe" (
        python\\python.exe app\\gui.py
    ) else (
        echo Error: Python not found. Please install Python 3.7+ or use the portable version.
        pause
        exit /b 1
    )
) else (
    echo Using system Python...
    python app\\gui.py
)

if %errorlevel% neq 0 (
    echo.
    echo Application encountered an error.
    pause
)
'''
    
    with open(os.path.join(package_dir, "run.bat"), 'w') as f:
        f.write(launcher_content)
    
    print("Created launcher script")
    
    # Create requirements file for portable installation
    requirements_content = '''PyQt5==5.15.9
reportlab==4.0.4
'''
    
    with open(os.path.join(package_dir, "requirements.txt"), 'w') as f:
        f.write(requirements_content)
    
    print("Created requirements file")
    
    # Create setup script
    setup_content = '''@echo off
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
'''
    
    with open(os.path.join(package_dir, "setup.bat"), 'w') as f:
        f.write(setup_content)
    
    print("Created setup script")
    
    # Create README
    readme_content = '''# Risk Assessment Tool - Portable Package

## Quick Start
1. Run `setup.bat` to install required packages (first time only)
2. Run `run.bat` to start the application

## System Requirements
- Windows 10 or later
- Python 3.7 or later (will be installed if not present)

## Installation Steps

### Step 1: Install Python (if not already installed)
- Download Python from https://python.org
- During installation, make sure to check "Add Python to PATH"
- Restart your computer after installation

### Step 2: Setup the Application
1. Double-click `setup.bat`
2. Wait for the installation to complete
3. Click any key when prompted

### Step 3: Run the Application
1. Double-click `run.bat`
2. The Risk Assessment Tool will start

## Features
- Create new risk assessments
- Load existing assessments
- Identify and categorize hazards
- Assess risk levels
- Generate PDF reports
- Manage control systems
- Plan alternative methods

## Troubleshooting

### "Python not found" error
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation
- Restart your computer after installation

### "pip not found" error
- Python installation may be incomplete
- Reinstall Python and ensure pip is included

### Application won't start
- Check that all requirements are installed: `python -m pip list`
- Try running setup.bat again
- Check Windows Event Viewer for error details

## File Locations
- Application files: app/
- Data files: data/
- Python packages: Installed in user directory

## Support
If you encounter issues, please contact your IT department or the application developer.
'''
    
    with open(os.path.join(package_dir, "README.txt"), 'w') as f:
        f.write(readme_content)
    
    print("Created README file")
    
    # Create desktop shortcut script
    shortcut_content = '''@echo off
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Risk Assessment Tool.lnk'); $Shortcut.TargetPath = '%~dp0run.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"
echo Shortcut created on desktop!
pause
'''
    
    with open(os.path.join(package_dir, "create_shortcut.bat"), 'w') as f:
        f.write(shortcut_content)
    
    print("Created shortcut creation script")
    
    # Create zip file
    print("Creating zip file...")
    zip_filename = "RiskAssessmentTool_Portable.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    print(f"Created {zip_filename}")
    
    print()
    print("=== Package Created Successfully! ===")
    print()
    print("Files created:")
    print(f"- {package_dir}/ (Portable package directory)")
    print(f"- {zip_filename} (Compressed package)")
    print()
    print("To deploy to your work computer:")
    print("1. Copy the zip file to your work computer")
    print("2. Extract the zip file")
    print("3. Run setup.bat (first time only)")
    print("4. Run run.bat to start the application")
    print("5. Optionally run create_shortcut.bat for desktop shortcut")

if __name__ == "__main__":
    create_portable_package() 