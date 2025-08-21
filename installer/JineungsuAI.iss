
#define MyAppName "Jineungsu AI"
#define MyAppVersion "18.2"
#define MyAppPublisher "Jineungsu Project"
#define MyAppURL "https://local"
#define MyAppExe "windows\start_jineungsu.bat"

[Setup]
AppId={{0D3AA5F5-3C9D-4F5C-9E89-FA2A9E5B18D2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={pf}\JineungsuAI
DefaultGroupName=Jineungsu AI
OutputDir=Output
OutputBaseFilename=JineungsuAI_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern

[Files]
Source: "..\jineungsu_ai\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Jineungsu AI 실행"; Filename: "{app}\{#MyAppExe}"
Name: "{commondesktop}\Jineungsu AI"; Filename: "{app}\{#MyAppExe}"

[Run]
Filename: "{app}\{#MyAppExe}"; Description: "설치 후 바로 실행"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\.venv"
Type: filesandordirs; Name: "{app}\mobile_inbox.jsonl"
Type: filesandordirs; Name: "{app}\clipboard_inbox.jsonl"
