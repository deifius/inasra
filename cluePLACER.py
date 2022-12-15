#!/usr/bin/env python3
import json, re
from os import system
from pdb import set_trace
from sys import argv

Job = '''
feed me :
	a partially constructed crossword puzzle in a 2d array (ipuz)
	& a word you want to place on the board,
	& the valid location for the first letter of the word x,y,
	only then will cluePLACER return the puzzle with the clue inserted
	zip* the board to do down!!
 '''

def loadargs():
	try:
		alexicon = argv[1]
		position = [int(argv[2]),int(argv[3])]
		try: orientation = argv[4]
		except: orientation = 'horiz'
		try: board = argv[5]
		except:
			with open("xwordspine.json") as readio: board =json.loads(readio.read())
	except:
		print(Job);
	return alexicon, board, position, orientation


def sanitize(alexicon, board, position):
	if len(alexicon) > len(board[0]) - position[1]:
		print("too long, submit shorter word")
		exit()
	if re.search("[^a-zA-Z ]", alexicon,) is None:
		alexicon = ''.join(alexicon.lower().split(' '))
		#set_trace()
		#print(f'alexicon, board, position {alexicon, board, position}')
		return alexicon.upper().replace(' ',''), board, position
	else:
		print("remove offending characters, submit l8ter")
		exit()

def insert(alexicon, board, position):
	#set_trace()
	regexalexicon = re.compile(''.join(board[position[0]][position[1]:position[1]+len(alexicon)]).replace(' ','.'))
	if regexalexicon.match(alexicon) is None:
		set_trace()
		print('\tnot fit')
		return 0
	for letter in alexicon:
		board[position[0]][position[1]] = letter
		position[1] = position[1]+1
	#for e in board: print(e)
	return board

def main():
	alexicon, board, position, orientation = loadargs()
	print(f'orientation: {orientation}')
	if orientation == 'vert': 	board = [list(row) for row in list(zip(*board))]
	insert(sanitize(alexicon, board, position))
	if orientation == 'vert': 	board = [list(row) for row in list(zip(*board))]
	print(json.dumps(board))
	with open(f'.NextMoves/{alexicon}.{orientation}.{str(position[0])}.{str(position[1])}', 'w') as writio: writio.write(json.dumps(board))

if __name__ == "__main__" : main()
