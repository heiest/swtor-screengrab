#SingleInstance, force
#include C:\Users\kyle.estes\Dropbox\Source\swtor-screengrab\CGdipSnapshot.ahk

workingDirectory := "C:\Users\kyle.estes\Dropbox\Source\swtor-screengrab\"
#If WinActive("ahk_exe swtor.exe")
Numpad3::
    WinGetActiveTitle, swtorWindowTitle
    WinGetPos, swtorWindowX, swtorWindowY, swtorWindowWidth, swtorWindowHeight, %swtorWindowTitle%
    MsgBox "SWTOR window at" %swtorWindowX%, %swtorWindowY%, %swtorWindowWidth%, %swtorWindowHeight%
    WinActivate %swtorWindowTitle%
    ImageSearch, foundX, foundY, %swtorWindowX%, %swtorWindowY%, %swtorWindowWidth%, %swtorWindowHeight%, "C:\Users\kyle.estes\Dropbox\Screenshots\Screenshot - 8_22_2020 , 6_54_12 PM.bmp"
    MsgBox Found at %foundX%, %foundY%
    WinActivate %swtorWindowTitle%
    return

#If WinActive("ahk_exe swtor.exe")
Numpad4::
    WinGetActiveTitle, swtorWindowTitle
    WinGetPos, swtorWindowX, swtorWindowY, swtorWindowWidth, swtorWindowHeight, %swtorWindowTitle%
    ;MsgBox %swtorWindowX%,%swtorWindowY%,%swtorWindowWidth%,%swtorWindowHeight%
    snap := new CGdipSnapshot(swtorWindowX, swtorWindowY, swtorWindowWidth, swtorWindowHeight)
    snap.TakeSnapshot()
    snap.SaveSnapshot(workingDirectory "1.bmp")
    return