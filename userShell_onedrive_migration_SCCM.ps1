# SCCM Discovery script
$RegPath = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
$OneDrivePath = "$env:USERPROFILE\OneDrive - COMPANY NAME / ONEDRIVE NAME"

# Check existing User Shell Folder settings
$ShellFolderSettings = Get-ItemProperty -Path $RegPath

$DesktopPath = $ShellFolderSettings.Desktop
$FavoritesPath = $ShellFolderSettings.Favorites
$MyMusicPath = $ShellFolderSettings."My Music"
$MyPicturesPath = $ShellFolderSettings."My Pictures"
$MyVideoPath = $ShellFolderSettings."My Video"
$PersonalPath = $ShellFolderSettings.Personal

if (($DesktopPath -eq "$env:USERPROFILE\Desktop") -and
    ($FavoritesPath -eq "$env:USERPROFILE\Favorites") -and
    ($MyMusicPath -eq "$env:USERPROFILE\Music") -and
    ($MyPicturesPath -eq "$env:USERPROFILE\Pictures") -and
    ($MyVideoPath -eq "$env:USERPROFILE\Videos") -and
    ($PersonalPath -eq "$env:USERPROFILE\Documents")) {
    
    # Exit script if existing User Shell Folder settings are for local profile
    return 1
} elseif (($DesktopPath -eq "$OneDrivePath\Desktop") -and
    ($MyPicturesPath -eq "$OneDrivePath\Pictures") -and
    ($PersonalPath -eq "$OneDrivePath\Documents")) {

    # Exit script if existing User Shell Folder settings are for OneDrive
    return 1
} else {
    return 0
}
#END SCCM Discovery Script

# SCCM remediation script
# runs if return from discovery is NOT 1
Add-Type -AssemblyName PresentationFramework
$RegPath = "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
# Delete User Shell Folders folder in registry
Remove-Item -Path $RegPath -Recurse -Force

# Restart explorer.exe and OneDrive
Stop-Process -Name explorer -Force
Stop-Process -Name OneDrive -Force
Start-Process -FilePath "C:\Windows\explorer.exe"
Try { Start-Process -FilePath "C:\Users\$Env:UserName\AppData\Local\Microsoft\OneDrive\OneDrive.exe" }
catch {
    #Write-Host "OneDrive already setup/signed in, launching from Program Files"
    Start-Process -FilePath "C:\Program Files\Microsoft OneDrive\OneDrive.exe"
}
[System.Windows.MessageBox]::Show("Sign into OneDrive from the icon in the bottom right of the screen.
    
Once Desktop, Documents, and Pictures have been selected for backup your files will return.", "Message from Systems Adminstrator", "OK", "Asterisk")
#END SCCM remediation script