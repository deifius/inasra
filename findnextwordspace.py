#!/usr/bin/env python3


import json
import re
from pdb import set_trace as st
from os import system
from sys import argv
import subprocess

''' feed me an partially constructed crossword puzzle in a 2d array, in ipuz notation (board)
 and a word (alexicon) you want to place on the board, and findthenextword will return a list of valid places
 in the format: [[xCoord_of_First_Letter,yCoord_of_First_Letter]] which is the first letter placement of the accross clue
 zip* the board to do down!!'''

def rotateboard(board):
	return [list(row) for row in list(zip(*board))]

def findnextwordspace (board, alexicon):
	''' feed me a board state and a word and I'll tell you all the horizontal spaces it legally fits'''
	def generate_faux_regex_lines(board):
		''' I break the board up into horizontal lines,
		 with '.' in any square that is not restricted by crossword rules
		 currently, I place too many '.' like on the tops of vertical words '''
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
		return lines
	def identify_legalplace(lines, alexicon):
		# I compare the faux_regex_lines to the alexicon
		obstacle = re.compile('\.?[a-z][a-z]+\.?')
		legalplace = []
		for line in enumerate(lines):
			validstart = len(line[1])-len(alexicon) - 1
			for validplace in range(validstart):
				valid_end = len(alexicon)+validplace
				if re.match(line[1][validplace:valid_end], alexicon) is not None:
					if re.search('[a-z| ]',line[1][validplace:valid_end],) is not None:
						if re.search('[a-z| ]',line[1][validplace-1],) is None:
							if validplace + len(alexicon) + 1 < len(line[1]):
								#validplace is valid for word!
								if re.search('[a-z| ]',line[1][valid_end+1],) is None:
									legalplace.append((line[0],validplace))
		return legalplace
	def find_goodplaces(legalplace, alexicon):
		''' this really should be a json hand off.
		where is processLegalPlaceItem defined?
		goodplaces = tuple(map(lambda item : processLegalPlaceItem(alexicon, item), legalplace))'''
		goodplaces = []
		for eachplace in legalplace:
			goodplaces.append('[[' + str(eachplace).replace('(','').replace(')','').replace(', ','],') + "], " + alexicon)
		return goodplaces
	goodplaces_for_alexicon = find_goodplaces(identify_legalplace(generate_faux_regex_lines(board),alexicon), alexicon)
	return goodplaces_for_alexicon

def sanitize(board, alexicon):
	if len(alexicon) > len(board[0]): exit()
	if re.search("[^a-zA-Z ]", alexicon,) is None:
		alexicon = ''.join(alexicon.lower().split(' '))
		return alexicon

def main():
	with open("xwordspine.json") as readio:
		board = json.loads(readio.read())
	alexicon = argv[1]
	#print(alexicon+ "\n\n\n")
	cleanexicon= sanitize(board, alexicon)
	#print('horiz:')
	horiz = findnextwordspace(board, cleanexicon)
	#print('vert:')
	vert = findnextwordspace(rotateboard(board), cleanexicon)
	''' vert is throwing real bad answers...  we need to work on this!'''
	#for each in vertboard: print(' '.join(each))
	st()
	#print('yo')
	for clue in horiz:
		subprocess.call(['python3', 'cluePLACER.py'] + clue.split(' ') + ['&'])
		#subprocess.call(['python3', 'clueonMTtable.py'] + clue.split(' ') + ['&'])
	for clue in vert:
		subprocess.call(['python3', 'cluePLACERvert.py'] + clue.split(' ') + ['&'])

if __name__ == "__main__" : main()
