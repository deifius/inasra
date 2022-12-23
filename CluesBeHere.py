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
					board[col[0]][row[0]] = '+'
			if abs(row[0] - position[1]) == 0:
				if board[col[0]][row[0]] == ' ':
					board[col[0]][row[0]] = '.'
			if abs(col[0] - position[0]) == 0:
				if board[col[0]][row[0]] == ' ':
					board[col[0]][row[0]] = '.'
				if abs(row[0] - position[1]) == 0:
					board[col[0]][row[0]] = '*'
	for e in board: e
	return board

def get2planes(zoard, position):
	'''i return two planes along the axes of the position'''
	board = show_cross(zoard, position)
	horiz = rotate(board[position[0]-1:position[0]+2])
	board = rotate(board)
	vert = rotate(board[position[1]-1:position[1]+2])
	return vert, horiz

def toss_non_viable(board):
	for e in enumerate(board):
		if e[1][1] == "*": break
		if e[1][0].isalnum():
			if not e[1][1].isalnum():
				board[e[0]][1] = '+'
		if e[1][2].isalnum():
			if not e[1][1].isalnum():
				board[e[0]][1] = '+'
	board.reverse()
	for e in enumerate(board):
		if e[1][1] == "*": break
		if e[1][0].isalnum():
			#print("letter on top")
			if not e[1][1].isalnum():
				#print(f"{'.'.join(e[1])}no letter inline: nonviable")
				board[e[0]][1] = '+'
				#print(f'board length:{len(board)}')
		if e[1][2].isalnum():
			if not e[1][1].isalnum():
				board[e[0]][1] = '+'
	board.reverse()
	board = rotate(board)[1]
	while '+' in board:
		if board.index('+') > board.index('*'):
			board = board[:board.index('+')]
		else: board = board[board.index('+')+1:]
	return ''.join(board) # longest possible regex in this place

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
