# CashDrawer
Open BT-100U Cash Drawer Driver Trigger using python on windows (Windows 10 and earlier due to driver limitations), MacOS, and linux for windows

There was a utility to do this bundled with the hardware but it turned out to be UI oriented (which I didn't prefer) and was just clunkier than I wanted.

The crux of the program is finding the correct COM port and writing the following characters to it: 27, 112, 0, 48

