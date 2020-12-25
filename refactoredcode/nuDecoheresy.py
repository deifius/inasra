#!/usr/bin/env python3

#	decoheresy is the time of inasra when the nebulous word cloud is distilled
#	and crystalized onto the board to create intricate and elaborate crossword puzzles
#	I am a combined cystalize/decoheresy/nextbestwords but stateless, 
#	pass me a json string which contains:
#		a word list
#		a board state
#		a coordinate
#	I will return all valid words from wordlist that
#	fits on the board and intersects the coordinate

from sys import argv
import json
import re
import pdb

class decoheresy:
	def __init__(self, wordlist, board, coordinate):
		self.wordlist = wordlist
		self.board = board
		self.coordinate = coordinate

	def forget(self, forget_word):
		self.wordlist.remove(forget_word)

	def addword(self, word, popularity):
		if word in self.wordlist:
			print('word already in lexicon, forget it to re-popularize')
		else:
			self.wordlist.insert(popularity, word)

	def set_coordinate(self, x, y):
		self.coordinate= [x,y]		

	def get_possibilities(self, howmany):
		for e in self.board: print(' '.join(e))	

#	def get_long_possibilities(self, howmany):
#	def get_short_possibilities(self, howmany):
#	def get_popular_possibilities(self, howmany):
#	def board_rotate(self):
#	def 

def sanitizer(argv):
	#	I sanitize the input, and break it down into wordlist, boardstate and coordinates
	#print(len(argv))
	if len(argv) == 2:
		wordlist, board, coordinate = json.loads(argv[-1])
	else:
		print("please specify one 3 element JSON list as input,\n1)\tword list\n2)\txword board\n3)\tcoordinate")
		exit(48)
	#print(','.join(wordlist))
	#print(re.compile('[^a-zA-Z]').search(''.join(wordlist)) is None)
	if type(wordlist) != list or re.compile('[^a-zA-Z]').search(''.join(wordlist)) != None:
		print('The word list must be a JSON list of strings, each string must be a valid xword value')
		exit(49)

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
		exit(50)
	thisboard = decoheresy(wordlist, board, coordinate)
	return thisboard

thisboard = sanitizer(argv)
#for e in json.loads(argv[-1]): print(e)
print(thisboard.coordinate)
#for e in board: print(e)
#print(','.join(coordinates))
pdb.set_trace()
