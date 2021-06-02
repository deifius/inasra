#!/usr/bin/env python3
import json
from pdb import set_trace
from sys import argv
#import subprocess
from glob import glob

# Yo I receive a coordinate in X Y format on the xwordspine board
# I construct a list of regular expressions for legal word configurations which intersect the coordinate provided
# I then compare the list to the freqygoodword list and return any matches
# a reference to a file in .NextMoves/

X = int(argv[1])
Y = int(argv[2])
boards_with_this_space = []
with open('xwordspine.json') as bookit:
		board = json.loads(bookit.read())
		if board[X][Y] != " ":
			print("got to handle this")
			exit(1)

for eachPossibleMove in glob('.NextMoves/*'):
	with open(eachPossibleMove) as possiboard: MTclue = json.loads(possiboard.read())
	if MTclue[X][Y] != " ":
				boards_with_this_space.append(str(eachPossibleMove))

print(json.dumps(boards_with_this_space))
