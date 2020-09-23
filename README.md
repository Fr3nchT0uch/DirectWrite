# DirectWrite
Command-line script to write binary files on an Apple DSK disk image.

© FRENCH TOUCH - 2019-2020
Code by Grouik/French Touch

DISCLAIMER: 
This Python script has been written to help Apple II cross-development on PC and is made to be executed from a command line. 
It is not optimized, probably buggy under certain circumstances and for someone who knows Python, the code is probably an abomination!
But it does the job. Use it at your own risk!


Write a binary file directly to an Apple II image disk (DSK)
Inputs (user or command line):
- DSK image file
- binary file
- first track  (in Hexa WITHOUT 0x,$ or anything)
- first sector (in Hexa WITHOUT 0x,$ or anything)
- writing direction (increasing / decreasing sector) (+ or -)
- Interleaving (D)os / (P)hysical / (F)ast Load

Output:
- modified DSK image file (warning: no backup!)

Command line example: `dw.py name.dsk binary.bin 0 A + d`
=> write binary.bin to name.dsk from track $0, sector $A, upward direction with dos interleaving.

All parameters (6) must be entered. There is no test performed on them.
You must know what you are doing!
