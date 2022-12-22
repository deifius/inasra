#!/usr/bin/env python3


import json
import re
from pdb import set_trace as st
from os import system
from sys import argv
import subprocess

''' feed me an partially constructed crossword puzzle
	in a 2d array, in ipuz notation (board)
 and a word (alexicon) you want to place on the board,
  findthenextword will return a list of valid places
 in the format: [[xCoord_of_First_Letter,yCoord_of_First_Letter]]
 which is the first letter placement of the accross clue

 zip* the board to do verts!!'''

def rotateboard(board):
	return [list(row) for row in list(zip(*board))]

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
	# print(board[0])
	for each in board:
		if re.search("[a-zA-Z]", "".join(each)) is not None:
			lines.append(''.join(each))
	print(lines)
	return lines

def identify_legalplace(lines, alexicon):
	"""I compare the faux_regex_lines to the alexicon"""
	obstacle = re.compile('\.?[a-z][a-z]+\.?')
	legalplace = []
	for pos, line in enumerate(lines):
		validstart = len(line) - len(alexicon) - 1
		for validplace in range(validstart):
			valid_end = len(alexicon) + validplace
			if re.match(line[validplace:valid_end], alexicon) is not None:
				if re.search('[a-z| ]', line[validplace:valid_end],) is not None:
					if re.search('[a-z| ]', line[validplace-1],) is None:
						if validplace + len(alexicon) + 1 < len(line):
							if re.search('[a-z| ]', line[valid_end+1],) is None:
								legalplace.append((pos, validplace))
	print(f"legal places:{legalplace}")
	return legalplace

def find_goodplaces(legalplaces, alexicon):
	# DEPRECATED, probably
	''' this really should be a json hand off.
	where is processLegalPlaceItem defined?
	goodplaces = tuple(map(lambda item : processLegalPlaceItem(alexicon, item), legalplace))'''
	goodplaces = []
	print("legalplaces", legalplaces)
	for eachplace in legalplaces:
		# goodplaces.append('[[' + str(eachplace).replace('(','').replace(')','').replace(', ','],') + "], " + alexicon)
		goodplaces.append('[' + str(eachplace).replace('(','').replace(')','').replace(', ',',') + "], " + alexicon)
		# goodplaces.append({"word: alexicon, pos: eachplace})
	return goodplaces

def findnextwordspace (board, alexicon):
	''' feed me a board state and a word and I'll tell you
		all the horizontal spaces it legally fits'''
	# goodplaces_for_alexicon = find_goodplaces(identify_legalplace(generate_faux_regex_lines(board),alexicon), alexicon)
	legalplaces_for_alexicon = identify_legalplace(generate_faux_regex_lines(board), alexicon)
	return legalplaces_for_alexicon

def sanitize(board, alexicon):
	if len(alexicon) > len(board[0]): exit()
	if re.search("[^a-zA-Z ]", alexicon,) is None:
		alexicon = ''.join(alexicon.lower().split(' '))
		return alexicon

def good_places_for(board, alexicon):
	cleanexicon = sanitize(board, alexicon)
	print(f'this cleanex:{cleanexicon}')
	return findnextwordspace(board, cleanexicon)

''' arg[1]: word (string), arg[2]: board (string[][] / xwordspine.json) '''
def main():
	try: board = argv[2]
	except:
		with open("xwordspine.json") as readio:
			board = json.loads(readio.read())
	alexicon = argv[1]
	cleanexicon = sanitize(board, alexicon)
	horiz = findnextwordspace(board, cleanexicon)
	vert = findnextwordspace(rotateboard(board), cleanexicon)
	'''# TODO: pass valid coords directly to browser for rendering / UI
	# TODO: pass all clues to cluePlacer in a dict, which performs all verts and horizes
	'''
	for clue in horiz:
		subprocess.call(['python3', 'cluePLACER.py'] + [alexicon, str(clue[0]), str(clue[1])])
		#subprocess.call(['python3', 'clueonMTtable.py'] + clue.split(' ') + ['&'])
	for clue in vert:
		subprocess.call(['python3', 'cluePLACER.py'] + [alexicon, str(clue[0]), str(clue[1]), 'vert'])
if __name__ == "__main__" : main()
