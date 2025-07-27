@echo off
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Risk Assessment Tool.lnk'); $Shortcut.TargetPath = '%~dp0run.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"
echo Shortcut created on desktop!
pause
