; INNO Setup script for crippy
; Copyright (C) 2023-2025 Ben Hattem (benghattem@gmail.com) - All Rights Reserved
#include "version.iss"
#define MyAppName "crippy"
#define MyCompany "benhattem.nl"
#define MyAppExe "crippy.exe"

[Setup]
AppId={{4923A51D-DB87-48D4-B564-681EF5C7E08D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher="{#MyCompany}"
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
DisableProgramGroupPage=true
LicenseFile="LICENSE"
OutputDir=dist
OutputBaseFilename="{#MyAppName} setup {#MyAppVersion}"
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile="python.ico"
UninstallDisplayIcon="{app}\{#MyAppExe}"
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:";
Name: desktopicon\common; Description: "For all users"; GroupDescription: "Additional icons:"; Flags: exclusive unchecked
Name: desktopicon\user; Description: "For the current user only"; GroupDescription: "Additional icons:"; Flags: exclusive
Name: quicklaunchicon; Description: "Create a &Quick Launch icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\build_info.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\{#MyAppName}\{#MyAppExe}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\{#MyAppName}\lib\*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Crippy"; Filename: "{app}\{#MyAppExe}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Crippy"; Filename: "{app}\{#MyAppExe}"; Tasks: desktopicon

[InstallDelete]
Type: filesandordirs; Name: "{app}\lib"
