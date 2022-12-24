#!/usr/bin/env python3
import json, re
from pdb import set_trace
from sys import argv
from glob import glob

description = '''
 Yo I receive a coordinate in X Y format on the xwordspine board
I construct a list of regular expressions for legal word
configurations which intersect the coordinate provided
I then compare the list to the freqygoodword list and return any matches
a reference to a file in .NextMoves/
'''

def rotate(board):
	return [list(row) for row in list(zip(*board))]

def show_cross(zoard, position):
	board = list(map(list, zoard))
	for row in enumerate(board):
		for col in enumerate(row[1]):
			if abs(col[0] - position[0]) > 1:
				if abs(row[0] - position[1]) > 1:
					board[col[0]][row[0]] = '%'
			if abs(row[0] - position[1]) == 0:
				if board[col[0]][row[0]] == ' ':
					board[col[0]][row[0]] = '.'
			if abs(col[0] - position[0]) == 0:
				if board[col[0]][row[0]] == ' ':
					board[col[0]][row[0]] = '.'
				if abs(row[0] - position[1]) == 0:
					board[col[0]][row[0]] = '*'
	for e in board[0]: e
	return board

def get2planes(zoard, position):
	'''i return two planes along the axes of the position'''
	board = show_cross(zoard, position)
	horiz = rotate(board[position[0]-1:position[0]+2])
	board = rotate(board)
	vert = rotate(board[position[1]-1:position[1]+2])
	return vert, horiz

def check_for_viability(regex):
	checkAlpha = re.compile('[a-zA-Z]')
	checkAster = re.compile('\*')
	if checkAlpha.findall(regex) and checkAster.findall(regex):
		#print("Regex is Viable for this crossword!")
		return True
	#print('Not viable regex for this board')
	return False

def return_max_regex(boardlet):
	"""	feed me a height 3 board of any width
		I will feed back the longest eachPossible
		regex for the middle row of the boardlet
	"""
	for e in enumerate(boardlet):
		if e[1][1] == "*": break
		if e[1][0].isalnum():
			if not e[1][1].isalnum():
				boardlet[e[0]][1] = '+'
		if e[1][2].isalnum():
			if not e[1][1].isalnum():
				boardlet[e[0]][1] = '+'
	boardlet.reverse()
	for e in enumerate(boardlet):
		if e[1][1] == "*": break
		if e[1][0].isalnum():
			#print("letter on top")
			if not e[1][1].isalnum():
				#print(f"{'.'.join(e[1])}no letter inline: nonviable")
				boardlet[e[0]][1] = '+'
				#print(f'boardlet length:{len(boardlet)}')
		if e[1][2].isalnum():
			if not e[1][1].isalnum():
				boardlet[e[0]][1] = '+'
	boardlet.reverse()
	boardlet = rotate(boardlet)[1]
	while '+' in boardlet:
		if boardlet.index('+') > boardlet.index('*'):
			boardlet = boardlet[:boardlet.index('+')]
		else: boardlet = boardlet[boardlet.index('+')+1:]
	regboards =  [''.join(boardlet)] # longest possible regex in this place
	if check_for_viability(regboards[0]) is False:
		return [] # no viable moves on this axis
	while len(regboards[-1]) > 1:
		new_regex = regboards[-1][1:] if regboards[-1][0] == '.' else regboards[-1][2:]
		if check_for_viability(new_regex) is False:
			return regboards
		for each in range(len(new_regex)):
			print(f"ya right: {new_regex[:each*-1]}")
			if check_for_viability(new_regex[:each*-1]) is True:
				if not new_regex[each*-1].isalpha():
					print('approved')
					regboards.append(new_regex[:each*-1])
				else: print(f"gotta skip it cuz last char was :{new_regex[each*-1]}")
		regboards.append(new_regex)
	return regboards

def main():
	X,Y = int(argv[1]), int(argv[2])
	if len(argv) == 4:
		board = argv[-1]
	else:
		with open('xwordspine.json') as bookit:
				board = json.loads(bookit.read())
				if board[X][Y] != " ":
					print("got to handle this")
					exit(1)

	boards_with_this_space = []
	set_trace()
	for eachPossibleMove in glob('.NextMoves/*'):
		with open(eachPossibleMove) as possiboard: MTclue = json.loads(possiboard.read())
		if MTclue[X][Y] != " ":
					boards_with_this_space.append(str(eachPossibleMove))

	print(json.dumps(boards_with_this_space))

if __name__ == '__main__': main()
