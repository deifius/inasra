#!/usr/bin/env python3

#	I am a stateless cystalize/decoheresy, pass me a json string which contains:
#		a word list
#		a board state
#		a coordinate
#	I will return all valid words from wordlist that
#	fits on the board and intersects the coordinate

from sys import argv
import json
import re

#print(len(argv))
if len(argv) == 2:
	wordlist, board, coordinate = json.loads(argv[-1])
else:
	print("please specify one 3 element JSON list as input,\n1)\tword list\n2)\txword board\n3)\tcoordinate")

#print(','.join(wordlist))
#print(re.compile('[^a-zA-Z]').search(''.join(wordlist)) is None)
if type(wordlist) != list or re.compile('[^a-zA-Z]').search(''.join(wordlist)) != None:
	print('The word list must be a JSON list of strings, each string must be a valid xword value')
	exit()

if type(board) is list and type(board[0]) is list and len(board[0][0]) is 1:
	for row in board:
		if len(row) != len(''.join(row)):
			print('the board must have one char in each coordinate,\n\tnone fewer or in excess.')
			exit()
	print('board is good')
else:
	print('formulate board as a 2d array like ipuz specifies.')

if type(coordinate) is list and type(coordinate[0]) is int and type(coordinate[1]) is int:
	if len(board) >= coordinate[0] and len(board[0]) >= coordinate[1]:
		print("coordinate is valid")
else:
	print('coordinates don\'t check out')
	exit()



