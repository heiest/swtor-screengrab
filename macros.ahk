#IfWinActive ahk_exe swtor.exe
^!+g::
; RunWait, pwsh -NoProfile -NoExit -Interactive -File .\Invoke-Python.ps1 check-lowest-prices, %A_ScriptDir%
RunWait, pwsh -NoProfile -NoExit -Interactive -File .\Invoke-Python.ps1 check-gtn --debug, %A_ScriptDir%
return

^!+o::
RunWait, pwsh -NoProfile -File .\Invoke-Python.ps1 inv-to-cargo, %A_ScriptDir%
return

^!+i::
RunWait, pwsh -NoProfile -File .\Invoke-Python.ps1 cargo-to-inv, %A_ScriptDir%
return

^!+b::
RunWait, pwsh -NoProfile -NoExit -Interactive -File .\Invoke-Python.ps1 open-crew-skills, %A_ScriptDir%
return
#IfWinActive

^!+p::
SendInput {Raw}cyc#shNER51B
return