#!/usr/bin/env python
""" Opens the BT-100U USB cash drawer interface. Detects platform as win32
or linux2. I'm unaware of linux drivers for the BT-100U but if they exist,
this will likely work on a native linux OS. This is coded to work with Linux
on Windows feature and windows as a primary OS.
"""
import multiprocessing
import time
import sys

def main():
    """ Open the drawer.
    """
    if sys.platform == "linux2":
        base = "/dev/ttyS"
    else:
        assert sys.platform == "win32"
        base = "COM"

    # COM ports can change and I didn't want to hardcode it so we just try each
    # of tem from 3-9
    for i in range(3, 9):
        try:
            with open('%s%d' % (base, i), 'w') as com:
                com.write(chr(27)+chr(112)+chr(0)+chr(48))
        except IOError:
            # COM/ttyS port likely was wrong
            pass

if __name__ == '__main__':
    proc = multiprocessing.Process(target=main, args=tuple())
    proc.start()
    # Max of 5 seconds to wait for drawer to open. Otherwise exit
    max_time = 5
    start_t = time.time()
    while time.time() <= start_t + max_time:
        if proc.is_alive():
            print ".",
            time.sleep(.1)
        else:
            break
    if proc.is_alive():
        proc.terminate()
