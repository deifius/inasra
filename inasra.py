#!/usr/bin/env python3
import json

class wordboard: #
	def __init__(self, origin, version, publisher, kind, copyright, author, title, intro, empty, dimensions, puzzle, clues, solution, history, lexicon, wordspace):
		self.origin = origin
		self.version = version
		self.kind = kind
		self.publisher = publisher
		self.copyright = copyright
		self.author = author
		self.title = title
		self.intro = intro
		self.empy = empty
		self.dimensions = dimensions
		self.puzzle = puzzle
		self.clues = clues
		self.solution = solution
		self.lexicon = lexicon #a list of relevant words ordered by relevance
		self.wordspace = wordspace #the list of words used in the order used.  This game is played by moving words from lexicon to wordspace
		self.history = history # the list of operations that have led to the current board state
	def resize(self): pass # sets dimensions of board
	def trim(self): pass # reduces board to minimal rectangle
	def findplaceword(self, word): pass # returns potential boardstates which include word
	def findfillspace(self, coordinates): pass # returns boardstates with a new word
	def visualize(self, xwordfield):
		#from os import system as systema; systema('clear')
		print('')
		for eachline in xwordfield:
			line = ' '
			linecheck = 0
			for each in eachline:
				line = line + ' ' + each
				if each != ' ':
					linecheck = 1
			if linecheck == 1:
				print(line)
	def show_solution(self):
		self.visualize(self.solution)
	def show_puzzle(self):
		self.visualize(self.puzzle)
	def rotate(self, board): # swaps horizontal and vertical faux_regex_lines
		return [list(row) for row in list(zip(*board))]
	def swap_down_across(self):
		self.clues['across','down'] = self.clues['down','across']
		self.solution = self.rotate(self.solution)
		self.puzzle = self.rotate(self.puzzle)
	def dumps(self):
		return json.dumps(self.__dict__)
	#@vertical
	#def vertical_operation(board):
	#	rotateboard(board)
	#def do_vertical(func):
	#	def wrapper_do_vertial():
	#		rotateboard()
	#		func()
	#		rotateboard()
	#	return wrapper_do_vertical
