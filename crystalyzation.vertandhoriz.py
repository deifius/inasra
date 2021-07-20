#!/usr/bin/env python3


import json
import re
from pdb import set_trace as st
from os import system
from sys import argv
import subprocess

# feed me an partially constructed crossword puzzle in a 2d array, in ipuz notation (board)
# and a word (alexicon) you want to place on the board, and findthenextword will return a list of valid places
# in the format: [[xCoord_of_First_Letter,yCoord_of_First_Letter]] which is the first letter placement of the accross clue
# zip* the board to do down!!

#set_trace()

def rotateboard(board):
	loard = list(zip(*board))
	for e in enumerate(loard):
		loard[e[0]] = list(e[1])
	return loard
def findnextwordspace (board, alexicon):
	# feed me a board state and a word and I'll tell you all the horizontal spaces it legally fits
	lines = []
	for space in enumerate(board[0]):
		if  board[0][space[0]] == ' ' and board[1][space[0]] == ' ':
			board[0][space[0]] = '.'
	for space in enumerate(board[-1]):
		if  board[-1][space[0]] == ' ' and board[-2][space[0]] == ' ':
			board[-1][space[0]] = '.'
	for eachline in enumerate(board):
		for space in enumerate(board[0]):
			if board[eachline[0]][space[0]] == ' ':
				if board[eachline[0]-1][space[0]] == '.' or board[eachline[0]-1][space[0]] == ' ':
					if board[eachline[0]+1][space[0]] == '.' or board[eachline[0]+1][space[0]] == ' ':
							board[eachline[0]][space[0]] = '.'
	for each in board:
		if re.search("[a-z]","".join(each)) is not None:
			lines.append(''.join(each))
	obstacle = re.compile('\.?[a-z][a-z]+\.?')
	legalplace = []
	for line in enumerate(lines):
		validstart = len(line[1])-len(alexicon) - 1
		#set_trace()
		for validplace in range(validstart):
			if re.match(line[1][validplace:len(alexicon)+validplace], alexicon) is not None:
				if re.search('[a-z| ]',line[1][validplace:len(alexicon)+validplace],) is not None:
					if re.search('[a-z| ]',line[1][validplace-1],) is None:
						if validplace + len(alexicon) + 1 < len(line[1]):
							if re.search('[a-z| ]',line[1][validplace+len(alexicon)+1],) is None:
								#validplace is valid for word!
								legalplace.append((line[0],validplace))
	goodplaces = []
	for eachplace in legalplace:
		goodplaces.append(alexicon + ' ' + str(eachplace).replace('(','').replace(')','').replace(',','').replace('[','').replace(']',''))
		print(alexicon + ' ' + str(eachplace).replace('(','').replace(')','').replace(',','').replace('[','').replace(']',''))
	print(alexicon + ' ' + str(legalplace).replace('(','').replace(')','').replace(',','').replace('[','').replace(']',''))
	print(json.dumps(goodplaces))
	#st()
	return goodplaces
def sanitize(board, alexicon):
	if len(alexicon) > len(board[0]):
		#print("too long, submit shorter word")
		exit()
	if re.search("[^a-zA-Z ]", alexicon,) is None:
		alexicon = ''.join(alexicon.lower().split(' '))
		return alexicon
	else:
		#print("remove offending characters, submit l8ter")
		exit()

def main():
	with open("xwordspine.json") as readio:
		board = json.loads(readio.read())
	alexicon = argv[1]
	#print(alexicon+ "\n\n\n")
	cleanexicon= sanitize(board, alexicon)
	horiz = findnextwordspace(board, cleanexicon)

	vertboard = [list(row) for row in list(zip(*board))]
	vert = findnextwordspace(vertboard, cleanexicon)
	#for each in vertboard: print(' '.join(each))
	for clue in horiz:
		subprocess.call(['python3', 'cluePLACER.py'] + clue.split(' ') + ['&'])
		#subprocess.call(['python3', 'clueonMTtable.py'] + clue.split(' ') + ['&'])
	for clue in vert:
		subprocess.call(['python3', 'cluePLACERvert.py'] + clue.split(' ') + ['&'])
		#subprocess.call(['python3', 'clueonMTtableVert.py'] + clue.split(' ') + ['&'])

if __name__ == "__main__" : main()
