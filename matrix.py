'''terminal visualizer a la The Matrix, with customization options'''
#! /usr/bin/env python3
# inspired by Joao S.O @ https://github.com/jsbueno/terminal_matrix

import shutil, time, sys, argparse
from random import randrange, choice

# print Command Sequence Initiator
prcs = lambda command: print("\x1b[",command, sep="", end="")
getchars = lambda start, end: [chr(i) for i in range(start,end)]

FPS = 20 
MAX_BLOBS = 150
MAX_SPEED = 9 
RAINBOW = False

def colors(position=1):
	# black,red,green,yellow,blue,magenta,cyan,white
	colors = [30,31,32,33,34,35,36,37]
	color = 0 
	if RAINBOW == True:
		color = choice(colors)
	elif position == 1:
		color = 37
	else:
		color = 32
	return color

def end():
	prcs("m") # reset attributes
	prcs("2J") # clear screen
	prcs("?25h") #unhide cursor
	print("printed %d rows and %d cols\n" % (ROWS, COLS))

def print_at(char,x,y,color=colors()):
	prcs("%d;%df" % (y,x)) # location
	prcs("%dm" % (color)) # formatting
	print(char,end="",flush=True) # actual print

def step_col(speed, tick, y):
	tick += 1
	if tick >= speed:
		y += 1
		tick = 0
	return tick, y

def generate_col(x):
	length = randrange(2,ROWS)
	speed = randrange(MAX_SPEED)
	espeed = randrange(MAX_SPEED)
	ticker = eticker = 0
	y = randrange(ROWS - length) + 1
	old_y = y - 1
	e_y =min(0, y - length)
	while True:
		ticker, y = step_col(speed, ticker, y)
		eticker, e_y = step_col(espeed, eticker, e_y)
		if 1 <= y and y <= ROWS:
			print_at(choice(CHARS),x,y,colors(1))
			print_at(choice(CHARS),x,old_y,colors(2))
		if 1 <= e_y and e_y <= ROWS:
			print_at(" ",x,e_y)
		if e_y > ROWS or e_y == y:
			print_at(" ",x,e_y)
			break
		old_y = y
		yield None

def iterate(screen):
	stopped = set()
	for blob in screen:
		try:
			next(blob)
		except StopIteration:
			stopped.add(blob)
	return stopped

def add_blobs(screen):
	if len(screen) < MAX_BLOBS:
		for i in range(MAX_BLOBS - len(screen)):
			screen.add(generate_col(randrange(COLS)))
		return True
	return False

def main():
	parser = argparse.ArgumentParser(description='terminal visualizer a la The Matrix')
	parser.add_argument("-c","--characters", \
		help="select the character set: choices are Hiragana, \
		Cyrillic, Latin, Greek, and Math",action='append')
	parser.add_argument("-r","--rainbow", help="turn on rainbow mode",action="store_true")
	args = parser.parse_args()
	
	chars = ""
	if args.characters:
		chars = args.characters[0] 
	global CHARS
	if chars.upper() == "CYRILLIC":
		CHARS = getchars(0x0400,0x051D)
	elif chars.upper() == "LATIN":
		CHARS = getchars(0x0041,0x005B)
	elif chars.upper()== "GREEK":
		CHARS = getchars(0x038E,0x03FF)
	elif chars.upper()== "MATH":
		CHARS = getchars(0x2200,0x22FF)
	elif chars.upper()== "HIRAGANA":
		CHARS = getchars(0x3047,0x3093)
	else:
		CHARS = getchars(0x30A1,0x30F6)
	CHARS += getchars(0x0030,0x0039)
	global ROWS, COLS, RAINBOW
	if args.rainbow:
		RAINBOW = args.rainbow
	COLS, ROWS = shutil.get_terminal_size()
	MAX_BLOBS = COLS - (COLS//4)
	prcs("?25l") # hide cursor
	prcs("2J") # clear screen
	print("\n",sep="",end="") # align to (1,1)
	screen = set()
	while True:
		while add_blobs(screen): pass
		stopped = iterate(screen)
		sys.stdout.flush()
		screen.difference_update(stopped)
		time.sleep(1/FPS)
	end()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		end()
