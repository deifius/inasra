#!/usr/bin/env python3

import json
import re
from pdb import set_trace
from os import system
from sys import argv

# feed me an partially constructed crossword puzzle in a 2d array, in ipuz notation (board)
# and the output of crystalization, 
# and crystalview will  return the puzzle with the clue inserted in all possible legal locations
# this does not change the actual board state, only shows possibilities
# zip* the board to do down!!

with open("xwordspine.json") as readio: board =json.loads(readio.read())

alexicon = argv[1]

positions = argv[2:]
posXY = []
while positions:
	posXY.append([int(positions.pop(0)), int(positions.pop(0))])

print(posXY)

def insert(alexicon, posXY):
	while posXY:
		position = posXY.pop(0)
		regexalexicon = re.compile(''.join(board[position[0]][position[1]:position[1]+len(alexicon)]).replace(' ','.'))
		print(position)
		if regexalexicon.match(alexicon) is None:
			print('this word does not fit the position you have specified')
			exit()
		for letter in alexicon:
			board[position[0]][position[1]] = '\033[1m' + letter + '\033[0m'
			position[1] = position[1]+1
	for e in board: print(''.join(e))

insert(alexicon, posXY)

#for e in board: ''.join(e)

#system("echo " + alexicon + ">> inasrafieldtest.txt")
