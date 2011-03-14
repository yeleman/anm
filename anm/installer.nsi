Name "Suivi des budgets ANM"

;SetCompress off 

; installer file name
OutFile "Install-ANM.exe"

; default destination dir
InstallDir "C:\ANM"

; request application privilege
; user should be ok. one can still right-click to install as admin
RequestExecutionLevel user

Page directory
Page instfiles

Section ""

  ; destination folder
  SetOutPath $INSTDIR
  
  ; List of files/folders to copy
  File /r dist\*.*
  File /r images
  File /r locale

  ; start menu entry
  CreateDirectory "$SMPROGRAMS\ANM"
  CreateShortCut "$SMPROGRAMS\ANM\Suivi budgets ANM.lnk" "$INSTDIR\anm.exe" "" "$INSTDIR\anm.exe" 0
  createShortCut "$SMPROGRAMS\ANM\Uninstall ANM.lnk" "$INSTDIR\uninstaller.exe"


  ; uninstaller
  writeUninstaller $INSTDIR\uninstaller.exe

SectionEnd

section "Uninstall"
 
# Always delete uninstaller first
delete $INSTDIR\uninstaller.exe

RMDir /r $SMPROGRAMS\ANM
 
# now delete installed file
delete $INSTDIR\*.exe
delete $INSTDIR\*.dll
delete $INSTDIR\*.exe
delete $INSTDIR\*.lib
delete $INSTDIR\*.zip
RMDir /r $INSTDIR\images
RMDir /r $INSTDIR\locale
 
sectionEnd

