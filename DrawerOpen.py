#!/usr/bin/env python3
""" Opens the BT-100U USB cash drawer interface. Detects platform as win32
or linux2. I'm unaware of linux drivers for the BT-100U but if they exist,
this will likely work on a native linux OS. This is coded to work with Linux
on Windows feature and windows as a primary OS.
"""
import multiprocessing
import time
import sys
import os

def common_send_code_to_file(filename):
    """ send the magic code to the filename specified.
         returns True if write succeeded, False otherwise
    """
    try:
        with open(filename, 'w') as com:
            com.write(chr(27)+chr(112)+chr(0)+chr(48))
            return True
    except IOError:
        pass
    return False

def common_findfile(base):
    """ function for windows/linux to scan for files based on known pattern.
    """
    for i in range(3, 9):
        common_send_code_to_file('%s%d' % (base, i))

def main_linux():
    """ No driver needed for linux.
    """
    base = "/dev/ttyS"
    common_findfile(base)

def main_win():
    """ Driver appears to have stopped working in the Windows 11 OS. Do not expect a
         patch from me.
    """
    base = 'COM'
    common_findfile(base)

def main_macos():
    """ MacOS doesn't appear to need a driver and instead uses a file in /dev named:
         'cu.usbserialXXX` with a unique number suffix.
    """
    base = '/dev/'
    filestart = 'cu.usbserial'
    for filename in os.listdir('/dev/'):
        if filename.startswith(filestart):
            common_send_code_to_file('%s%s' % (base, filename))

def main():
    """ Detect OS and stub out to os specific function
    """
    if sys.platform == 'linux2':
        main_linux()
    elif sys.platform == 'darwin':
        main_macos()
    else:
        assert sys.platform == 'win32'
        main_win()

if __name__ == '__main__':
    proc = multiprocessing.Process(target=main, args=tuple())
    proc.start()
    # Max of 5 seconds to wait for drawer to open. Otherwise exit
    max_time = 5
    start_t = time.time()
    while time.time() <= start_t + max_time:
        if proc.is_alive():
            print('.', end='')
            time.sleep(.1)
        else:
            break
    if proc.is_alive():
        proc.terminate()
