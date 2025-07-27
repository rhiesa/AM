#!/usr/bin/env python3
"""
Build script for Risk Assessment Tool
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Install required packages for building"""
    print("Installing build requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib',
        'reportlab.platypus',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'reportlab.pdfbase',
        'reportlab.pdfbase.ttfonts',
        'reportlab.pdfbase.pdfmetrics',
        'dataclasses',
        'enum',
        'typing',
        'json',
        'pickle',
        'pathlib',
        'datetime'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='RiskAssessmentTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('RiskAssessmentTool.spec', 'w') as f:
        f.write(spec_content)
    
    print("Created PyInstaller spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Build using spec file
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller", 
        "--clean", 
        "RiskAssessmentTool.spec"
    ])
    
    print("Build completed successfully!")

def create_installer_script():
    """Create a simple installer script for the work computer"""
    installer_content = '''@echo off
echo Installing Risk Assessment Tool...
echo.

REM Create installation directory
if not exist "%USERPROFILE%\\RiskAssessmentTool" mkdir "%USERPROFILE%\\RiskAssessmentTool"

REM Copy executable
copy "RiskAssessmentTool.exe" "%USERPROFILE%\\RiskAssessmentTool\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Risk Assessment Tool.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\\RiskAssessmentTool\\RiskAssessmentTool.exe'; $Shortcut.Save()"

echo.
echo Installation completed!
echo The Risk Assessment Tool is now available on your desktop.
echo.
pause
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content)
    
    print("Created installer script (install.bat)")

def create_readme():
    """Create a README file for the packaged application"""
    readme_content = '''# Risk Assessment Tool - Standalone Package

## Installation Instructions

### Option 1: Simple Installation (Recommended)
1. Copy the entire folder to your work computer
2. Double-click `install.bat` to install the application
3. The application will be installed to your user folder and a shortcut will be created on your desktop

### Option 2: Manual Installation
1. Copy `RiskAssessmentTool.exe` to any folder on your work computer
2. Double-click the executable to run the application

## System Requirements
- Windows 10 or later
- No additional software installation required (Python not needed)

## Features
- Create new risk assessments
- Load existing assessments
- Identify and categorize hazards
- Assess risk levels
- Generate PDF reports
- Manage control systems
- Plan alternative methods

## Usage
1. Launch the application
2. Choose to create a new assessment or load an existing one
3. Fill in project and company information
4. Use the tabs to:
   - Identify hazards
   - Assess risks
   - Define control systems
   - Plan alternative methods
5. Generate PDF reports when complete

## File Formats
- Assessment files are saved in JSON format
- Reports are generated as PDF files
- All data is stored locally on your computer

## Support
If you encounter any issues, please contact your IT department or the application developer.

## Version
This is a standalone version of the Risk Assessment Tool.
'''
    
    with open('README.txt', 'w') as f:
        f.write(readme_content)
    
    print("Created README file")

def main():
    """Main build process"""
    print("=== Risk Assessment Tool - Build Process ===")
    print()
    
    try:
        # Install requirements
        install_requirements()
        print()
        
        # Create spec file
        create_spec_file()
        print()
        
        # Build executable
        build_executable()
        print()
        
        # Create installer
        create_installer_script()
        print()
        
        # Create README
        create_readme()
        print()
        
        print("=== Build Process Completed Successfully! ===")
        print()
        print("Files created:")
        print("- dist/RiskAssessmentTool.exe (Main executable)")
        print("- install.bat (Installation script)")
        print("- README.txt (Instructions)")
        print()
        print("To deploy to your work computer:")
        print("1. Copy the entire 'dist' folder contents")
        print("2. Copy install.bat and README.txt")
        print("3. Transfer to your work computer")
        print("4. Run install.bat on the work computer")
        
    except Exception as e:
        print(f"Error during build process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 