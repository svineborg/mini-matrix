# /usr/bin/env python3

import shutil, sys, time
from random import choice, randrange, paretovariate

# print Command Sequence
prcs = lambda command: print("\x1b[",command, sep="", end="")
getchars = lambda start, end: [chr(i) for i in range(start,end)]

#original is mirrored half-width katakana, unavailable in UTF-8
# so, next best thing is full-width

katakana = getchars(0xFF66,0xFF9D)
latin = getchars(0x0030,0x0039)
chars = katakana + latin

def clear_screen():
	prcs("2J")
	print("")

def init():
	global rows, cols
	rows, cols = shutil.get_terminal_size()
	clear_screen()
	prcs("?25l") # hide cursor

def print_at(x, y, char):
	prcs("%d;%df" % (y,x) + char) # line, column, character to print

def gen_col():
	return [chars[randrange(1,len(chars))] for i in range(0,rows)]

def print_col(col,x):
	for i in range(1,len(col)):
		print_at(x * 2, i, col[i]) #half-width chars need double spacing for fullscreen

def print_screen():
	for i in range(1,cols):
		col = gen_col()
		print_col(col,i)

def end():
	prcs("m") # reset attributes
	clear_screen()
	prcs("?25h") # unhide cursor
	print("printed %d rows and %d cols\n" % (rows, cols))

if __name__ == "__main__":
	init()
	try:
		while(True):
			print_screen()
	except KeyboardInterrupt:
		end()
