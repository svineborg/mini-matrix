# /usr/bin/env python3

# inspired by Joao S.O. 
# https://github.com/jsbueno/terminal_matrix

import shutil
from random import randrange

# print Command Sequence
prcs = lambda command: print("\x1b[",command, sep="", end="")
getchars = lambda start, end: [chr(i) for i in range(start,end)]

# using half-width katakana like the original

katakana = getchars(0xFF66,0xFF9D)
latin = getchars(0x0030,0x0039)
chars = katakana + latin

def clear_screen():
	prcs("2J")
	print("")

def init():
	global rows, cols
	rows, cols = shutil.get_terminal_size()
	cols = cols * 2 # halfwidth chars so double the columns
	clear_screen()
	prcs("?25l") # hide cursor

def print_at(x, y,color,brightness,char):
	prcs("%d;%df" % (y,x)) # location
	prcs("%d;%dm" % (color, brightness)) #formatting
	print(char,end="",sep="") # actual print

def gen_col():
	return [chars[randrange(1,len(chars))] for i in range(0,rows)]

def print_col(col,x):
	for i in range(1,len(col)):
		print_at(x * 2 - 1, i, 32, randrange(1,2), col[i]) #start at 1 but add buffer column between

def print_screen():
	for i in range(1,cols):
		col = gen_col()
		print_col(col,i)

def end():
	prcs("m") # reset attributes
	clear_screen()
	prcs("?25h") # unhide cursor
	print("printed %d rows and %d cols\n" % (rows, cols))

def main():
	while True:
		print_screen()

def run():
	init()
	main()

if __name__ == "__main__":
	try:
		run()
	except KeyboardInterrupt:
		end()
