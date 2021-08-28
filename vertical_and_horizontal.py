#!/usr/bin/env python3

def rotateboard(board):
	return [list(row) for row in list(zip(*board))]



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
	def rotate(self): pass # swaps horizontal and vertical faux_regex_lines
	def rotate(self): # swaps horizontal and vertical faux_regex_lines
		return [list(row) for row in list(zip(*board))]
	def findplaceword(self, word): pass # returns potential boardstates which include word
	def findfillspace(self, coordinates): pass # returns boardstates with a new word
	#@vertical
	#def vertical_operation(board):
	#	rotateboard(board)
	#def do_vertical(func):
	#	def wrapper_do_vertial():
	#		rotateboard()
	#		func()
	#		rotateboard()
	#	return wrapper_do_vertical
