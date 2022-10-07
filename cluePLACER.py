#!/usr/bin/env python3
import json
import re
#from pdb import set_trace
from os import system
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
		except: pass
		try: board = argv[5]
		except:
			with open("xwordspine.json") as readio: board =json.loads(readio.read())
	except:
		print(Job);
	return alexicon, position, board


def sanitize(alexicon, board, position):
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

def insert(alexicon, position, board):
	#set_trace()
	regexalexicon = re.compile(''.join(board[position[0]][position[1]:position[1]+len(alexicon)]).replace(' ','.'))
	if regexalexicon.match(alexicon) is None:
		print(','.join(argv) +'\tnot fit')
		exit()
	for letter in alexicon:
		board[position[0]][position[1]] = letter
		position[1] = position[1]+1
	#for e in board: print(e)

def main():
	alexicon, position, board = loadargs()
	insert(sanitize(alexicon, board, position), position, board)
	with open('.NextMoves/'+alexicon+".HORIZ."+str(position[0])+'.'+str(position[1]), 'w') as writio:
		writio.write(json.dumps(board))

if __name__ == "__main__" : main()
