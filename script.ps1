cd "C:\Users\jcsolano\OneDrive - Intel Corporation\Documents\Engagements\POC\Power Apps\msapp\Migration\PowerAppsMigrator\Input\msapp"
$AppName = (Get-Item -Path "*" -Include "*.msapp").BaseName
Rename-Item -Path ".\$AppName.msapp" -NewName ".\$AppName.zip"
Expand-Archive -Path ".\$AppName.zip"
Remove-Item -Path ".\$AppName.zip"