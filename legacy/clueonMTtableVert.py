#!/usr/bin/env python3
import json
import re
from pdb import set_trace
from os import system
from sys import argv
import subprocess

# feed me an partially constructed crossword puzzle in a 2d array, in ipuz notation (board)
# and a word (alexicon) you want to place on the board, the valid location for the first letter of the word x,y,
# and clueonMTtable will provide the clue on an otherwise empty board, for overlaying on the existing board.
# zip* the board to do down!!


with open("xwordspine.json") as readio: board =json.loads(readio.read())

alexicon = argv[1]
position = [int(argv[2]),int(argv[3])]


def sanitize(alexicon):
	if len(alexicon) > len(board[0]) - position[1]:
		print("too long, submit shorter word")
		exit()
	if re.search("[^a-zA-Z ]", alexicon,) is None:
		alexicon = ''.join(alexicon.lower().split(' '))
		#set_trace()
		return alexicon
	else: 
		print("remove offending characters, submit l8ter")
		exit()

def insert(alexicon, position):
	regexalexicon = re.compile(''.join(board[position[0]][position[1]:position[1]+len(alexicon)]).replace(' ','.'))
	if regexalexicon.match(alexicon) is None:
		print('this word does not fit the position you have specified')
		exit()
	#set_trace()# This is where we empty the board 
	for row in enumerate(board):
		for space in enumerate(row[1]):
			#print(space)
			board[row[0]][space[0]] = ' '
	#for row in board: print(row)

	for letter in alexicon:
		board[position[0]][position[1]] = letter
		position[1] = position[1]+1
	#for e in board: print(e)

board = [list(row) for row in list(zip(*board))] 
insert(sanitize(alexicon), position)
board = [list(row) for row in list(zip(*board))] 

FileNameOut = '.NextMoves/'+alexicon+".MTtable.VERT."+str(position[0])+'.'+str(position[1])
#print(FileNameOut)
with open(FileNameOut, 'w') as writio:
	writio.write(json.dumps(board))

#print(['python3', 'BoardImgDrawer.py', FileNameOut, ['&']])
#subprocess.call(['python3', 'BoardImgDrawer.py', FileNameOut, json.dumps(board)])


