#!/usr/bin/env python3
import json
from findnextwordspace import findnextwordspace
import db
from pdb import set_trace
from os import system
from whiptail import Whiptail
from lorem import text as lorem
import Acronymizer
import Start_New_inasra
import wikichompdb
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
		self.lexicon = lexicon # a list of relevant words ordered by relevance. The relephant herd.
		self.wordspace = wordspace # the list of words used in the order used.  This game is played by moving words from lexicon to wordspace
		self.history = history # the list of operations that have led to the current board state
	def resize(self, width, height):
		print(f"old width & height:  {self.dimensions['width']}, {self.dimensions['height']}")
		while len(self.solution[0]) > width:
			for each_row in self.solution: each_row.pop()
		while len(self.solution[0]) < width:
			self.add_one_col_Across()
		while len(self.solution) > height:
			self.solution.pop()
		while len(self.solution) < height:
			self.add_one_row_Down()
		self.dimensions['width'], self.dimensions['height'] = width, height
		print(f'{width}, {height}')
		print(f"new width & height:  {self.dimensions['width']}, {self.dimensions['height']}")
		self.show_solution()
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
		self.show_solution()
	def find_places_for(self, word):
		'''returns potential boardstates which include word'''
		def find_horizontal_solutions():
			return findnextwordspace(self.solution, word)
		def find_vertical_solutions():
			self.solution = self.rotate(self.solution)
			what_you_wanna_know = find_horizontal_solutions()
			self.solution = self.rotate(self.solution)
			return what_you_wanna_know
		decohere = find_horizontal_solutions()
		decohere = decohere + find_vertical_solutions()
		return decohere
	def find_words_for(self, coordinates):
		raise InsertCheeseErr("some day I'll return a list of boardstates with a new word intersecting the given coordinates")
	def visualize(self, xwordfield):
		print("+ " * len(xwordfield[0]) + "+ +")
		for each_line in xwordfield:
			print(f"+ {' '.join(each_line)} +")
		print("+ " * len(xwordfield[0]) + "+ +")
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
		self.show_solution()
	def dumps(self):
		return json.dumps(self.__dict__, indent=2) # export state as json string
	def add_one_row_Down(self):
		new_empty_row = ['.' for each_row in self.solution[0]]
		#for each in self.solution[0]: new_empty_line.append('.')
		self.solution.append(new_empty_row)
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
	def range_word(self, word, fist_char_position):
		pass # returns a list of the range of the word
	def add_word_horiz(self, word, Across, Down):
		self.clues['Across'].append(word)
		word = list(word)
		while word:
			self.add_character(word.pop(0), Across, Down)
			Across += 1
	def add_word_vert(self, word, Across, Down):
		self.clues['Down'].append(word)
		word = list(word)
		while word:
			self.add_character(word.pop(0), Across, Down)
			Down += 1
	def add_word(self, position, word, **kwargs):
		try:
			if type(position[0]) is list and type(position[1]) is int: self.add_word_horiz(word, position[0][0], position[1])
			if type(position[1]) is list and type(position[0]) is int: self.add_word_vert(word, position[0], position[1][0])
		except:
			print('submit an inasra monad')
			return -1
		self.lexicon.append(word)
	def db_word_obj(self, dat_word_tho):
		word_tuples = db.db_query('''
			SELECT id FROM word WHERE word = ?
		''', dat_word_tho)
		if word_tuples:
			return word_tuples[0]
		return None
		# word_tuple = word_tuples[0]
		# return {"id": word_tuple[0]}
	def Start(self):
		is_context_cli = True # Hardcoded for now
		if is_context_cli:
			new_adventure = Whiptail()
			new_adventure.title = "inasra welcomes you"
			new_adventure.backtitle = lorem()
			word, exitstatus = new_adventure.inputbox('what shall you offer to inasra?')
			system("ps -ef|grep visualise | grep -v grep || xterm -e  './visualizations/bashvisualise.py'")
		else: pass # we were called by a web browser TODO

		inasraid = db.db_insert("inasra", name = word, height = 0, width = 0)
		choice_pos = 0

		# Chomp the starting word
		wikified_word = wikichompdb.wiki_query_prep(word)
		wikichompdb.wikipedia_grab_chomp(wikified_word)
		word_obj = self.db_word_obj(wikified_word)
		if word_obj is None:
			print(f'we tried real hard, but db_word_obj failz0red: {word}')

		prev_inasra_word_id = db.db_insert("inasra_words",
			word_id = word_obj["id"],
			direction = 'x',
			x = 0,
			y = 0,
			inasra_id = inasraid,
			char_pos = choice_pos,
			prev_word_id = None
		)
		prev_inasra_words = db.db_query("SELECT id, direction, x, y, char_pos FROM inasra_words WHERE id = ?", prev_inasra_word_id)
		prev_inasra_word = prev_inasra_words[0]
		# prev_word_obj = {"id": prev_word_tuple[0], "direction": prev_word_tuple[1], "x": prev_word_tuple[2], "y": prev_word_tuple[3]}

		# wikified_word = WikiChomp.wiki_query_prep(word)
		# WikiChomp.wikipedia_grab_chomp(wikified_word)

		while choice_pos > -1:
			print("we startz da loop "+word)

			wikified_word = wikichompdb.wiki_query_prep(word)
			wikichompdb.wikipedia_grab_chomp(wikified_word)
			relephant = Acronymizer.get_relephant(wikified_word)
			acronym_words = Acronymizer.acronymize(wikified_word, relephant)

			choice_pos = Acronymizer.get_choice_with_whiptail(word, acronym_words, relephant)
			if choice_pos < 0: break
			choice_word = acronym_words[choice_pos].split('    ')[-1]

			wikified_choice_word = wikichompdb.wiki_query_prep(choice_word)
			wikichompdb.wikipedia_grab_chomp(wikified_choice_word)

			if is_context_cli:
				word_obj = self.db_word_obj(wikified_choice_word)
				direction = "y" if prev_inasra_word["direction"] == "x" else "x"
				x = prev_inasra_word["x"]
				y = prev_inasra_word["y"]
				# FIXME: assigning character positions is off by 1
				# eg, row #30 has the correctly values for row #29
				# (see inasra #47)
				if prev_inasra_word["direction"] == "x":
					x = x + prev_inasra_word["char_pos"]
				else: # direction == "y"
					y = y + prev_inasra_word["char_pos"]
				inasra_word_id = db.db_insert("inasra_words",
					word_id = word_obj["id"],
					direction = direction,
					x = x,
					y = y,
					inasra_id = inasraid,
					char_pos = choice_pos,
					prev_word_id = prev_inasra_word["id"]
				)

				# Prep word for the next pass
				prev_inasra_words = db.db_query("SELECT id, direction, x, y, char_pos FROM inasra_words WHERE id = ?", inasra_word_id)
				prev_inasra_word = prev_inasra_words[0]
				# prev_word_obj = {"id": prev_word_tuple[0], "direction": prev_word_tuple[1], "x": prev_word_tuple[2], "y": prev_word_tuple[3]}
				word = choice_word

				# go fetch the selected word from WP, so it's in the database
				# wikified_word = WikiChomp.wiki_query_prep(word)
				# WikiChomp.wikipedia_grab_chomp(wikified_word)

				print("next loop plz "+word)

				# TODO: update inasra's height and width here
			else: pass # we probably bail back to user with list of words to pick
		# end while

		# TODO FIXME: do x, y, and direction, and also word_order
		# convert spinylize
		# linkid = db.db_insert("inasra_words", inasra_id = inasraid, word_id = choice_word_ids[0].id, x = 0, y = 0, direction = 'x')

		#self.Start_New_inasra.main()

def main():
	with open('emptyinasra.ipuz') as fill: ths = inasra(**json.loads(fill.read()))
	ths.Start()

if __name__ == "__main__": main()
