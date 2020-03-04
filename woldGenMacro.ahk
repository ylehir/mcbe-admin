#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;==================================================================================================

#NoEnv

^!g::
	offset := 16*12*2
	start := -4096
	stop := 4096
	startOffset := 0
	Loop
	{
		currX := start + startOffset
		Loop
		{ 
			currZ := start + startOffset
			Loop
			{
				Send {Enter}
				Sleep 100
				Send /tp
				Send {space}
				Sleep 100
				Send %currX% 100 %currZ%
				Sleep 100
				Send {Enter}
				Sleep 6000
				if (currZ >= stop)
					break
				if (BreakLoop = 1)
					break
				currZ := currZ + offset
			}
			if ( currX >= stop ) 
				break
			currX := currX + offset
			if (BreakLoop = 1)
				break
		}
		if (startOffset > 0)
			break
		startOffset := 16*12
		if (BreakLoop = 1)
					break
	}
	BreakLoop = 0
Return

; Pressing pause will stop it
Pause::
	BreakLoop = 1
return