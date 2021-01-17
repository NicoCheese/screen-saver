#include <Timers.au3>
While 1
   Sleep(10)
   $idleTimer = _Timer_GetIdleTime()
   If $idleTimer > 300000 And Not WinExists("ScreenSaverThingy") Then
      ShellExecute("ScreenSaver.pyw")
      WinWait("ScreenSaverThingy")
   ElseIf $idleTimer < 10 Then
      WinClose("ScreenSaverThingy")
   EndIf
WEnd