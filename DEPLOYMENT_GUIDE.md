# Risk Assessment Tool - Deployment Guide

This guide provides multiple options for packaging and deploying your Risk Assessment Tool to work computers.

## Option 1: Standalone Executable (Recommended for IT-restricted environments)

### Prerequisites
- Python 3.7+ installed on your development machine
- Internet connection for downloading PyInstaller

### Steps

1. **Install PyInstaller** (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script**:
   ```bash
   python build_exe.py
   ```

3. **Deploy to work computer**:
   - Copy the entire `dist` folder contents
   - Copy `install.bat` and `README.txt`
   - Transfer to work computer
   - Run `install.bat` on the work computer

### Advantages
- No Python installation required on work computer
- Single executable file
- Works in IT-restricted environments
- Professional appearance

### Disadvantages
- Larger file size (~50-100MB)
- May trigger antivirus warnings
- Requires admin rights for installation

## Option 2: Portable Python Package (Recommended for flexible deployment)

### Steps

1. **Run the portable package script**:
   ```bash
   python package_simple.py
   ```

2. **Deploy to work computer**:
   - Copy `RiskAssessmentTool_Portable.zip` to work computer
   - Extract the zip file
   - Run `setup.bat` (first time only)
   - Run `run.bat` to start the application

### Advantages
- Smaller file size (~5-10MB)
- No admin rights required
- Easy to update
- Works with existing Python installations

### Disadvantages
- Requires Python on work computer
- Multiple files to manage

## Option 3: Manual Python Installation

### Steps

1. **Create a requirements file**:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Deploy to work computer**:
   - Copy `gui.py`, `risk_assessment.py`, and `requirements.txt`
   - Install Python 3.7+ on work computer
   - Run: `pip install -r requirements.txt`
   - Run: `python gui.py`

### Advantages
- Minimal file transfer
- Full control over environment
- Easy debugging

### Disadvantages
- Requires Python knowledge
- Manual setup process
- May conflict with existing Python installations

## System Requirements

### Minimum Requirements
- Windows 10 or later
- 4GB RAM
- 100MB free disk space
- Internet connection (for initial setup)

### Recommended Requirements
- Windows 11
- 8GB RAM
- 500MB free disk space
- High-speed internet connection

## Installation Scenarios

### Scenario 1: IT-Managed Environment
- **Recommended**: Option 1 (Standalone Executable)
- **Process**: Submit executable to IT for approval and deployment
- **Considerations**: May require code signing and antivirus whitelisting

### Scenario 2: User-Controlled Environment
- **Recommended**: Option 2 (Portable Package)
- **Process**: Users can install themselves with minimal IT involvement
- **Considerations**: Requires Python installation permission

### Scenario 3: Development/Testing Environment
- **Recommended**: Option 3 (Manual Installation)
- **Process**: Direct Python development environment
- **Considerations**: Best for testing and development

## Troubleshooting

### Common Issues

#### "Application won't start"
- Check Windows Event Viewer for error details
- Verify all dependencies are installed
- Try running from command line to see error messages

#### "Python not found"
- Install Python from https://python.org
- Ensure "Add Python to PATH" is checked during installation
- Restart computer after installation

#### "Permission denied"
- Run as administrator (for standalone executable)
- Check antivirus settings
- Verify file permissions

#### "Missing DLL errors"
- Install Visual C++ Redistributable
- Update Windows
- Reinstall the application

### Debug Mode

To run in debug mode for troubleshooting:

```bash
# For portable package
python app/gui.py

# For standalone executable
RiskAssessmentTool.exe --debug
```

## Security Considerations

### Antivirus Software
- Standalone executables may trigger false positives
- Submit to antivirus vendor for whitelisting
- Use code signing certificates for enterprise deployment

### Network Security
- Application runs locally, no network communication
- PDF reports may contain sensitive data
- Consider encryption for saved files

### Data Privacy
- All data stored locally on user's computer
- No data transmitted to external servers
- Consider backup strategies for assessment files

## Updates and Maintenance

### Version Management
- Include version number in application title
- Create changelog for updates
- Provide migration path for existing data

### Distribution
- Use internal file sharing or intranet
- Consider automated deployment tools
- Provide rollback procedures

### Support
- Create user documentation
- Establish support contact
- Monitor for common issues

## Performance Optimization

### Startup Time
- Minimize imports in main module
- Use lazy loading for heavy components
- Optimize resource loading

### Memory Usage
- Close file handles properly
- Clear large objects when not needed
- Monitor memory usage during PDF generation

### File I/O
- Use efficient file formats
- Implement proper error handling
- Consider compression for large files

## Testing Checklist

Before deploying to work computers, test:

- [ ] Application starts without errors
- [ ] All features work correctly
- [ ] PDF generation works
- [ ] File save/load functions work
- [ ] No memory leaks during extended use
- [ ] Works on different Windows versions
- [ ] Compatible with common antivirus software
- [ ] No network connectivity issues
- [ ] Proper error handling and user feedback
- [ ] Accessibility features work (if applicable)

## Legal and Compliance

### Software Licensing
- Ensure all dependencies are properly licensed
- Include license information in distribution
- Consider open source license for your application

### Data Protection
- Comply with relevant data protection regulations
- Implement proper data handling procedures
- Consider data retention policies

### Audit Trail
- Log important actions for compliance
- Maintain version history
- Document configuration changes

## Conclusion

Choose the deployment option that best fits your organization's requirements and constraints. The portable package (Option 2) is generally the most flexible and user-friendly approach for most environments.

For enterprise deployment, consider working with your IT department to establish proper procedures for software distribution and maintenance. 