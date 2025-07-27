#!/usr/bin/env python3
"""
Simple script to build a standalone executable for Risk Assessment Tool
"""

import os
import sys
import subprocess
import shutil

def build_standalone_exe():
    """Build a standalone executable using PyInstaller"""
    print("=== Building Standalone Risk Assessment Tool ===")
    print()
    
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    print("Building standalone executable...")
    
    # Build command with all necessary options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=RiskAssessmentTool",    # Executable name
        "--clean",                      # Clean cache
        "--noconfirm",                  # Don't ask for confirmation
        "gui.py"                        # Main script
    ]
    
    try:
        subprocess.check_call(cmd)
        print("Build completed successfully!")
        
        # Check if executable was created
        exe_path = os.path.join("dist", "RiskAssessmentTool.exe")
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
            print(f"Executable created: {exe_path}")
            print(f"File size: {file_size:.1f} MB")
            
            # Create a simple README for the executable
            readme_content = '''# Risk Assessment Tool - Standalone Executable

## Quick Start
1. Double-click "RiskAssessmentTool.exe" to run the application
2. No installation or setup required!

## System Requirements
- Windows 10 or later
- 4GB RAM minimum
- 100MB free disk space

## Features
- Create new risk assessments
- Load existing assessments
- Identify and categorize hazards
- Assess risk levels
- Generate PDF reports
- Manage control systems
- Plan alternative methods

## Usage
1. Launch the application by double-clicking the executable
2. Choose to create a new assessment or load an existing one
3. Fill in project and company information
4. Use the tabs to complete your risk assessment
5. Generate PDF reports when complete

## File Formats
- Assessment files are saved in JSON format
- Reports are generated as PDF files
- All data is stored locally on your computer

## Troubleshooting
- If the application won't start, try running as administrator
- Check Windows Event Viewer for error details
- Ensure you have sufficient disk space and memory

## Support
If you encounter any issues, please contact your IT department or the application developer.
'''
            
            with open("dist/README.txt", 'w') as f:
                f.write(readme_content)
            
            print("Created README.txt in dist folder")
            
            print()
            print("=== Deployment Ready! ===")
            print()
            print("To deploy to your work computer:")
            print("1. Copy 'RiskAssessmentTool.exe' to your work computer")
            print("2. Copy 'README.txt' (optional, for instructions)")
            print("3. Double-click the executable to run")
            print()
            print("That's it! No installation, no setup, no batch files needed.")
            
        else:
            print("Error: Executable was not created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = build_standalone_exe()
    if not success:
        sys.exit(1) 