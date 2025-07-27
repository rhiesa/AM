# Quick Start Guide - Risk Assessment Tool Deployment

## 🚀 Ready to Deploy!

Your Risk Assessment Tool has been packaged and is ready for deployment to your work computer.

## 📦 What Was Created

1. **`RiskAssessmentTool_Portable.zip`** - The main package file
2. **`RiskAssessmentTool_Portable/`** - Unpackaged directory (same contents)
3. **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment guide
4. **`build_exe.py`** - Script to create standalone executable (if needed)

## 🎯 Recommended Approach: Portable Package

### Step 1: Transfer to Work Computer
- Copy `RiskAssessmentTool_Portable.zip` to your work computer
- Extract the zip file to any folder (e.g., Desktop or Documents)

### Step 2: First-Time Setup
1. Double-click `setup.bat`
2. Wait for Python packages to install
3. Click any key when prompted

### Step 3: Run the Application
1. Double-click `run.bat`
2. The Risk Assessment Tool will start

### Step 4: Create Desktop Shortcut (Optional)
1. Double-click `create_shortcut.bat`
2. A shortcut will be created on your desktop

## 🔧 Alternative: Standalone Executable

If you prefer a single executable file (no Python required):

1. Run: `python build_exe.py`
2. Copy the `dist` folder contents to your work computer
3. Run `install.bat` on the work computer

## 📋 System Requirements

- **Windows 10 or later**
- **4GB RAM minimum** (8GB recommended)
- **100MB free disk space**
- **Internet connection** (for first-time setup only)

## 🆘 Troubleshooting

### "Python not found"
- Download Python from https://python.org
- Check "Add Python to PATH" during installation
- Restart your computer

### "Application won't start"
- Check that setup.bat completed successfully
- Try running `python app/gui.py` from command line
- Check Windows Event Viewer for errors

### "Permission denied"
- Right-click and "Run as administrator"
- Check antivirus settings
- Ensure you have write permissions to the folder

## 📞 Support

If you encounter issues:
1. Check the `README.txt` file in the package
2. Review `DEPLOYMENT_GUIDE.md` for detailed instructions
3. Contact your IT department if needed

## 🎉 Success!

Once deployed, you'll have a professional risk assessment tool that can:
- Create comprehensive risk assessments
- Generate PDF reports
- Manage hazard identification
- Track control systems
- Plan alternative methods

The application runs completely offline and stores all data locally on your computer. 