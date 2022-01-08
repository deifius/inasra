#!/usr/bin/env python3
import json
from findnextwordspace import findnextwordspace
import db
from pdb import set_trace
import Start_New_inasra
#from inasra import inasra as inasra lol

class inasra: #
	def __init__(self, origin, version, kind, copyright, author, publisher, title, intro, empty, dimensions, puzzle, clues, solution, lexicon, wordspace, history):
		self.origin = origin
		self.version = version
		self.kind = kind
		self.copyright = copyright
		self.author = author
		self.publisher = publisher
		self.title = title
		self.intro = intro
		self.empty = empty
		self.dimensions = dimensions
		self.puzzle = puzzle
		self.clues = clues
		self.solution = solution # the operating word board
		self.lexicon = lexicon # a list of relevant words ordered by relevance
		self.wordspace = wordspace # the list of words used in the order used.  This game is played by moving words from lexicon to wordspace
		self.history = history # the list of operations that have led to the current board state
	def resize(self, board, Across, Down): pass # sets dimensions of board
	def trim_solution(self):
		'''reduces board to minimal rectangle'''
		def trim_oneD():
			keep_trimming = True
			for each in self.solution[-1]:
				if each != '.':
					keep_trimming = False
			if keep_trimming:
				self.solution.pop(-1)
				self.trim_solution()
		trim_oneD()
		self.solution = self.rotate(self.solution)
		trim_oneD()
		self.solution = self.rotate(self.solution)
	def find_places_for(self, word):
		'''returns potential boardstates which include word'''
		def find_horizontal_solutions():
			return findnextwordspace(self.solution, word)
		def find_vertical_solutions():
			self.solution = self.rotate(self.solution)
			what_you_wanna_know = find_horizontal_solutions()
			self.solution = self.rotate(self.solution)
			return what_you_wanna_know
		#print('horiz:')
		decohere = find_horizontal_solutions()
		set_trace()
		#print('vert:')
		decohere = decohere + find_vertical_solutions()
		return decohere
	def find_words_for(self, coordinates): pass # returns boardstates with a new word intersecting the given coordinates
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
		print('')
	def show_solution(self):
		self.visualize(self.solution)
	def show_puzzle(self):
		self.visualize(self.puzzle)
	def rotate(self, board): # returns a board swapped horiz & vert axes
		return [list(row) for row in list(zip(*board))]
	def swap_down_across(self):
		self.clues['Down'], self.clues['Across'] = self.clues['Across'], self.clues['Down']
		self.dimensions['height'],self.dimensions['width']=self.dimensions['width'],self.dimensions['height']
		self.solution = self.rotate(self.solution)
		self.puzzle = self.rotate(self.puzzle) # rotates all elements and produces the mirror xord
	def dumps(self):
		return json.dumps(self.__dict__, indent=2) # export state as json string
	def add_one_row_Down(self):
		new_empty_line = []
		for each in self.solution[0]: new_empty_line.append('.')
		self.solution.append(new_empty_line)
		self.dimensions['height'] += 1
	def add_one_col_Across(self):
		for each_row in self.solution: each_row.append('.')
		self.dimensions['width'] += 1
	def check_space(self, Across, Down):
		if isinstance(Across, list):
			space = ''
			for each_space in Across:
				try:
					space += self.check_space(each_space, Down)
				except IndexError:
					return "Board too narrow: add col Across"
			return space #a matchable regex
		if isinstance(Down, list):
			space = ''
			for each_space in Down:
				try:
					space += self.check_space(Across, each_space)
				except IndexError:
					return "Board too shallow: add row Down"
			return space #a matchable regex
		if isinstance(Across, int) and isinstance(Down, int):
			return self.solution[Down][Across]
	def add_character(self, character, Across, Down):
		self.solution[Down][Across] = character
	def range_word(self, word, fist_char_position): pass # returns a list of the range of the word
	def add_word_horiz(self, word, Across, Down):
		self.clues['Across'].append(word)
		while word:
			self.add_character(list(word).pop(0), Across, Down)
			Across += 1

	def add_word_vert(self, word, Across, Down):
		letters = list(word)
		while letters:
			self.add_character(letters.pop(0), Across, Down)
			Down += 1
		self.clues['Down'].append(word)
	def add_word(self, position, word, **kwargs):
		try:
			if type(position[0]) is list and type(position[1]) is int: self.add_word_horiz(word, position[0][0], position[1])
			if type(position[1]) is list and type(position[0]) is int: self.add_word_vert(word, position[0], position[1][0])
		except:
			print('submit an inasra monad')
			return -1
		self.lexicon.append(word)
	def Start(self):
		self.Start_New_inasra.main()
