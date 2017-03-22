
;This file is part of PyVot.
;
; Copyright (C) 2016 Cédrick FAURY
;
;PyVot is free software; you can redistribute it and/or modify
;it under the terms of the GNU General Public License as published by
;the Free Software Foundation; either version 2 of the License, or
;(at your option) any later version.
;
;PyVot is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
;MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;GNU General Public License for more details.
;
;You should have received a copy of the GNU General Public License
;along with PyVot; if not, write to the Free Software
;Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

[ISPP]
#define AppName "pyVot"
#define AppVersion "0.6.2"
#define AppVersionInfo "0.6.2"
#define AppVersionBase "06"

#define AppURL "https://github.com/cedrick-f/pyVot"


[Setup]
;Informations générales sur l'application
AppName={#AppName}
AppVerName={#AppName} {#AppVersion}
AppVersion={#AppVersion}
AppPublisher=Cédrick Faury
AppCopyright=Copyright © 2006-2017 Cédrick Faury
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}

;Répertoire de base contenant les fichiers
SourceDir=C:\Users\Cedrick\Documents\Developp\pyVot

;Repertoire d'installation
DefaultDirName={pf}\{#AppName}
DefaultGroupName={#AppName}
LicenseFile=LICENSE.txt

;Paramètres de compression                               
;lzma ou zip
Compression=lzma/max
SolidCompression=yes
;Par défaut, pas besoin d'être administrateur pour installer
PrivilegesRequired=none
;Nom du fichier généré et répertoire de destination
OutputBaseFilename=setup_{#AppName}_{#AppVersionInfo}_win32
OutputDir=releases

UninstallDisplayIcon={app}\images\pyvot.ico
;Fenêtre en background
WindowResizable=false
WindowStartMaximized=true
WindowShowCaption=true
BackColorDirection=lefttoright
WizardImageFile = Images\grand_logo.bmp
WizardSmallImageFile = Images\petit_logo.bmp

[Languages]
Name: fr; MessagesFile: "compiler:Languages\French.isl"

[CustomMessages]
;
; French
;
fr.uninstall=Désinstaller
fr.gpl_licence=Prendre connaissance du contrat de licence pour le logiciel
fr.fdl_licence=Prendre connaissance du contrat de licence pour la documentation associée
fr.CreateDesktopIcon=Créer un raccourci sur le bureau vers
fr.AssocFileExtension=&Associer le programme {#AppName} aux extensions .pyv
fr.CreateQuickLaunchIcon=Créer un icône dans la barre de lancement rapide

fr.FileExtension={#AppName}.montage
fr.FileExtensionName=Montage de roulements pyVot

fr.InstallFor=Installer pour :
fr.AllUsers=Tous les utilisateurs
fr.JustMe=Seulement moi
fr.ShortCut=Raccourcis :
fr.Association=Association de fichier :

[Messages]
BeveledLabel=PyVot installation

[Files]
;
; Fichiers de la distribution
;
Source: src\build\*.*; DestDir: {app}; Flags : ignoreversion recursesubdirs;
;Source: D:\Documents\Developpement\PyVot 0.6\src\dist\*.*; DestDir: {app}\bin; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\*.txt; DestDir: {app}; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\donnees\*.txt; DestDir: {app}\Donnees; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\aide\pyvotaide.chm; DestDir: {app}\Aide; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\aide\html; DestDir: {app}\Aide\html; Flags : ignoreversion recursesubdirs createallsubdirs;
;Source: D:\Documents\Developpement\PyVot 0.6\images\*.*; DestDir: {app}\Images; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\images\Arbre_Alesage\*.*; DestDir: {app}\Images\Arbre_Alesage; Flags : ignoreversion;
;S;ource: D:\Documents\Developpement\PyVot 0.6\images\Arrets\*.*; DestDir: {app}\Images\Arrets; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\images\Joints\*.*; DestDir: {app}\Images\Joints; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\images\Roulements\*.*; DestDir: {app}\Images\Roulements; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\images\Schema\*.*; DestDir: {app}\Images\Schema; Flags : ignoreversion;
;Source: D:\Documents\Developpement\PyVot 0.6\exemples\*.*; DestDir: {app}\Exemples; Flags : ignoreversion;

[Tasks]
Name: desktopicon2; Description: {cm:CreateDesktopIcon} {#AppName} ; GroupDescription: {cm:ShortCut}; MinVersion: 4,4
Name: fileassoc; Description: {cm:AssocFileExtension}; GroupDescription: {cm:Association};
Name: common; Description: {cm:AllUsers}; GroupDescription: {cm:InstallFor}; Flags: exclusive
Name: local;  Description: {cm:JustMe}; GroupDescription: {cm:InstallFor}; Flags: exclusive unchecked

[Icons]
Name: {group}\{#AppName}; Filename: {app}\bin\pyvot.exe; WorkingDir: {app}\bin; IconFileName: {app}\bin\pyvot.exe
Name: {group}\Aide {#AppName}; Filename: {app}\aide\pyvotaide.chm; Comment: Aide en ligne; IconFileName: {app}\aide\pyvotaide.chm
Name: {group}\Désinstaller {#AppName}; Filename: {app}\unins000.exe;IconFileName: {app}\unins000.exe
;
; On ajoute sur le Bureau l'icône PyVot
;
Name: {userdesktop}\{#AppName};   Filename: {app}\bin\pyvot.exe; WorkingDir: {app}\bin; MinVersion: 4,4; Tasks: desktopicon2; IconFileName: {app}\bin\pyvot.exe

[_ISTool]
Use7zip=true

[Registry]
; Tout ce qui concerne les fichiers .pyv
Root: HKCR; SubKey: "{cm:FileExtension}"; ValueType: string;  ValueName: ""; ValueData: "{cm:FileExtensionName}";  Flags: uninsdeletekey
Root: HKCR; Subkey: "{cm:FileExtension}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\bin\Images\fichier-pyv.ico,0"; Flags: uninsdeletekey
Root: HKCR; SubKey: "{cm:FileExtension}\Shell\Open"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\bin\pyvot.exe"; Flags: uninsdeletekey
Root: HKCR; SubKey: "{cm:FileExtension}\Shell\Open\Command"; ValueType: string; ValueName: ""; ValueData: """{app}\bin\pyvot.exe"" ""%1"""; Flags: uninsdeletekey
Root: HKCR; Subkey: ".pyv"; ValueType: string; ValueName: ""; ValueData: "{cm:FileExtension}"; Flags: uninsdeletevalue

; Pour stocker le style d'installation : "All users" ou "Current user"
Root: HKLM; Subkey: SOFTWARE\{#AppName}; Flags: uninsdeletekey
Root: HKLM; Subkey: SOFTWARE\{#AppName}; ValueType: string; ValueName: DataFolder; ValueData: {code:DefAppDataFolder}\{#AppName} ; Flags: uninsdeletekey
Root: HKLM; Subkey: SOFTWARE\{#AppName}; ValueType: string; ValueName: UninstallPath ; ValueData: {uninstallexe}; Flags: uninsdeletekey

;Root: HKCR; SubKey: .pyv; ValueType: string; ValueData: Projet PyVot; Flags: uninsdeletekey
;Root: HKCR; SubKey: Projet PyVot; ValueType: string; Flags: uninsdeletekey; ValueData: Projet PyVot
;Root: HKCR; SubKey: Projet PyVot\Shell\Open\Command; ValueType: string; ValueData: """{app}\bin\pyvot.exe"" ""%1"""; Flags: uninsdeletekey;
;Root: HKCR; Subkey: Projet PyVot\DefaultIcon; ValueType: string; ValueData: {app}\Images\fichier-pyv.ico,0; Flags: uninsdeletekey;
; et une clef pour indiquer que pyvot est installé
;Root: HKLM; Subkey: SOFTWARE\PyVot; Flags: uninsdeletekey;
;Root: HKLM; Subkey: SOFTWARE\PyVot; ValueName: "UninstallPath" ; ValueType: string; ValueData: {uninstallexe}; Flags: uninsdeletekey;


[code]
function PyVotInstalled():Boolean;
begin
  if RegKeyExists(HKEY_LOCAL_MACHINE,'SOFTWARE\PyVot\') then
    Result:=True
  else if RegKeyExists(HKEY_CLASSES_ROOT,'.pyv') then
    Result:=True
  else
    Result:=False;
end;


function GetUninstallPath(): String;
var
  ResultPath: String;
begin
  if RegQueryStringValue(HKEY_LOCAL_MACHINE,'SOFTWARE\PyVot\','UninstallPath', ResultPath) then
    Result := ResultPath
  else
    Result := ExpandConstant('{pf}\PyVot\unins000.exe')
End;


function NextButtonClick(CurPageID: Integer): Boolean;
var
  ResultCode: integer;
begin
  if (CurPageID = wpWelcome) and (PyVotInstalled()) then
    if MsgBox('Une précédente version de PyVot est déja installée !'#13 +
              'Il est conseillé de la desinstaller.'#13#13 +
              'Vouler vous désinstaller la version précédente de PyVot ?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      if Exec(GetUninstallPath(), '', '', SW_SHOW,
              ewWaitUntilTerminated, ResultCode) then
        begin
          // handle success if necessary; ResultCode contains the exit code
        end
        else
        begin
          MsgBox('La désinstallation automatique de PyVot à échouée !'#13#13 +
                 'Veuillez désinstaller la version précédente de PyVot manuellement.', mbCriticalError, MB_OK);
          // handle failure if necessary; ResultCode contains the error code
        end;
    end;
  Result := True;
end;



procedure DesinstallerPyVot();
begin
  if MsgBox('Une précédente version de PyVot est déja installée ! Il est conseillé de la desinstaller. Vouler vous désinstaller PyVot avant d''en installer une nouvelle version ?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      //
    end;
end;

{ Renvoie le dossier "Application Data" à utiliser }
function DefAppDataFolder(Param: String): String;
begin
  if IsTaskSelected('common') then
    Result := ExpandConstant('{commonappdata}')
  else
    Result := ExpandConstant('{localappdata}')
end;

//function InitializeSetup(): Boolean;
//begin
//  if PyVotInstalled then
//    Msgbox('Une précédente version de PyVot est déja installée ! Désinstaller PyVot avant d'en installer une nouvelle version.',mbConfirmation,MB_Ok);
//end;

//function GetPSPadPath(Default: String) : String;
//begin
//   RepPSPad:=Copy(RepPSPad,2,Length(RepPSPad)-1);
//   Result:=ExtractFilePath(RepPSPad);
//end;
