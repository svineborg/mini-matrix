# /usr/bin/env python3

# inspired by Joao S.O @ https://github.com/jsbueno/terminal_matrix

import shutil, time, sys
from random import randrange, choice, paretovariate

# global variables
MAX_SPEED = 10 
FRAMES_PER_SECOND = 33
MAX_BLOBS = 250 

# print Command Sequence
prcs = lambda command: print("\x1b[",command, sep="", end="")
getchars = lambda start, end: [chr(i) for i in range(start,end)]

# using half-width katakana + latin numerals
chars =  getchars(0xFF66,0xFF9D) + getchars(0x0030,0x0039)

def clear_screen():
	prcs("2J") # clear screen
	print("\n") # align cursor to (1,1)

def init():
	global rows, cols
	cols, rows = shutil.get_terminal_size()
	cols += 1
	rows += 1
	clear_screen()
	prcs("?25l") # hide cursor

def print_at(char,x,y,bright=0,color=0):
	prcs("%d;%df" % (y,x)) # location
	#bright: 0, 1 = normal, bold
	prcs("%d;%dm" % (bright,color)) # formatting
	print(char,end="",flush=True) # actual print

def step_column(speed, tick, y):
	tick += 1
	if tick >= speed:
		y += 1
		tick = 0
	return tick, y

def gen_col(x):
	white = 37
	green = 32
	normal = 0
	bold = 1
	faded = 2
	speed = randrange(1,MAX_SPEED)
	espeed = randrange(1,MAX_SPEED)
	y = counter = ecounter = 0
	oldline = eline = -1
	erasing = False
	length =  paretovariate(rows) * rows
	while True:
		counter, y = step_column(speed, counter,y)
		if y < length:
			print_at(choice(chars),x,y,bold,white)
			print_at(choice(chars),x,y-1,bold,green)
			print_at(choice(chars),x,y-2,normal,green)
			print_at(choice(chars),x,y - (length//4),faded,green)
		if eline <= length:
			print_at(" ",x,eline)
			ecounter, eline = step_column(espeed, ecounter, eline)
		yield None
		eline = x - length
		oldline = y
		if y >= length:
			print_at(" ",x, y)
			break

def iterate(cascading):
	stopped = set()
	for c in cascading:
		try:
			next(c)
		except StopIteration:
			stopped.add(c)
	return stopped

def add_new(cascading):
	if randrange(MAX_BLOBS + 1) > len(cascading) :
		x = randrange(cols)
		for i in range(randrange(MAX_BLOBS)) : 
			cascading.add(gen_col((x + i) % cols))
		return True
	return False

def main():
	cascading = set()
	while True:
		while add_new(cascading): pass
		stopped = iterate(cascading)
		sys.stdout.flush()
		cascading.difference_update(stopped)
		time.sleep(1/FRAMES_PER_SECOND)

def end():
	prcs("m") # reset attributes
	clear_screen()
	prcs("?25h") # unhide cursor
	print("printed %d rows and %d cols\n" % (rows, cols))

def test(test_name):
	if test_name == "printing":
		for x in range(1,cols):
			for y in range(1,rows):
				print_at(chars[1],x,y)
		print("done testing printing")
	if test_name == "cascade":
		print("done testing cascade")

if __name__ == "__main__":
	try:
		init()
		if len(sys.argv) > 1:
			test(sys.argv[1])
		else:
			main()
		end()
	except KeyboardInterrupt:
		end()
