#!/usr/bin/env python3

import json
import findnextwordspace
import db
from pdb import set_trace
from os import system
from whiptail import Whiptail
from lorem import text as lorem
import Acronymizer
import Start_New_inasra
import wikichompdb
from CrystalizeByCoords import return_max_regex, turn_match_to_board,compare_freqy_to_regboards,get2planes
from collections import OrderedDict

#from inasra import inasra as inasra lol

class inasra: #
	def __init__(self, origin, version, kind, copyright, author, publisher, title, intro, empty, dimensions, puzzle, clues, solution, lexicon, wordspace, history, inasraid, *args, **kwargs):
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
		try: self.inasraid = inasraid
		except:
			if hasattr(self, 'inasraid') == False:
				self.inasraid = None
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
				return findnextwordspace.findnextwordspace(self.solution, word)
		def find_vertical_solutions():
			self.solution = self.rotate(self.solution)
			what_you_wanna_know = find_horizontal_solutions()
			self.solution = self.rotate(self.solution)
			return what_you_wanna_know
		decohere = find_horizontal_solutions()
		decohere = decohere + find_vertical_solutions()
		return decohere
	def find_words_for(self, coords):
		"""
			I return a list of word places that
			include the coordinates [coords]
			& intersect the existing xword solution
			resulting in a new legal xword
		"""
		if not self.lexicon: self.set_lexicon()
		vert, horiz = get2planes(self.solution, coords)
		this, that = return_max_regex(horiz), return_max_regex(vert)
		vick, huck = compare_freqy_to_regboards(self.lexicon,that),compare_freqy_to_regboards(self.lexicon,this)
		vertical_words = [turn_match_to_board(coords, e, 'vert') for e in vick]
		horizontal_words = [turn_match_to_board(coords, e, 'horiz') for e in huck]
		crystal_eyes = {
			'vertical_words':vertical_words,
			'horizontal_words': horizontal_words
		}
		return crystal_eyes
	def visualize(self, xwordfield):
		print("+ " * len(xwordfield[0]) + "+ +")
		for each_line in xwordfield:
			print(f"+ {' '.join(each_line)} +")
		print("+ " * len(xwordfield[0]) + "+ +")
	def show_solution(self):
		self.visualize(self.solution)
	def show_puzzle(self):
		self.visualize(self.puzzle)
	def rotate(self, board): #if you are readin this you want to us swap_down_across()
		"""returns a board swapped horiz & vert axes"""
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
	def check_space(self, Down, Across):
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
	def add_character(self, character, Down, Across):
		self.solution[Down][Across] = character
	def range_word(self, word, fist_char_position):
		pass # returns a list of the range of the word
	def add_word_horiz(self, word, Down, Across):
		self.clues['Across'].append(word)
		word = list(word)
		while word:
			self.add_character(word.pop(0), Down, Across)
			Across += 1
	def add_word_vert(self, word, Down, Across):
		self.clues['Down'].append(word)
		word = list(word)
		while word:
			self.add_character(word.pop(0), Down, Across)
			Down += 1
	def add_word(self, position, word, **kwargs):
		try:
			if type(position[0]) is list and type(position[1]) is int: self.add_word_horiz(word, position[0][0], position[1])
			if type(position[1]) is list and type(position[0]) is int: self.add_word_vert(word, position[0], position[1][0])
		except:
			print('submit an inasra monad')
			return -1
		self.lexicon.append(word)
	def imagine(self, *args): # I'll show the board with a word you supply
		try:
			word, coords, orientation = args
		except:
			print('please supply word, coords, orientation')
			return -1
		try:
			reality_board = list(map(list, self.solution))
			if "VERT" in orientation.upper():
				self.add_word_vert(word, *coords)
			else:
				self.add_word_horiz(word, *coords)
			imaginary_board = list(map(list, self.solution))
			self.show_solution()
			self.solution = reality_board
			return imaginary_board
		except: return -2
		"""	if we do a few things like
		db.write.word, remove.from.lexicon, add.history
		then we can just self.solution = imaginary_board!
		"""
	def db_word_obj(self, dat_word_tho):
		word_tuples = db.db_query('''
			SELECT id FROM word WHERE word = ?
		''', dat_word_tho)
		if word_tuples:
			return word_tuples[0]
		return None
		# word_tuple = word_tuples[0]
		# return {"id": word_tuple[0]}
	def write_self_to_db(self):
		self.inasraid = db.db_insert("inasra", name = self.title)
	def write_word_to_db(self, word):
		print("You done called a deprecated func: write_word_to_db")
		word_obj = self.db_word_obj(word)
		if not word_obj or not self.inasraid:
			return None
		last_inasra_word = db.get_last_inasra_word(self.inasraid)
		if last_inasra_word:
			x = 0 # TODO
			y = 0 # TODO
			direction = 'y' if last_inasra_word.direction == 'x' else 'x'
			prev_word_id = last_inasra_word.id
		else:
			x = 0
			y = 0
			direction = 'x'
			prev_word_id = None
		return db.db_insert("inasra_words",
			word_id = word_obj["id"],
			inasra_id = self.inasraid,
			direction = direction,
			x = x,
			y = y,
		)
	def set_lexicon(self):
		#raise InsertCheeseErr('''
		#			This could be wordlistpreparer.main() but thaxt is in serious need of refactoring
		#			desired inputs: glob of every article reference from every word in the spine of the board
		#			desired output: a set of links ordered by redundancy in list, minus words already on board
		#		''')
		spinewords = self.history
		for each in spinewords:
			wikichompdb.wikipedia_grab_chomp(each)
		links_to_spine = db.get_multiwords_links(spinewords) # every link in every article for every word in the spine
		#import pdb; pdb.set_trace()
		sorted_by_frequency = sorted(links_to_spine, key = links_to_spine.count,reverse = True)
		ordered_set = list(OrderedDict.fromkeys(sorted_by_frequency))
		for each_word in spinewords:
			try: ordered_set.remove(each_word)
			except: print(f"perhaps {each_word} is already part of the xword")
		self.lexicon = ordered_set
		return self.lexicon
	def crystalize_imagine(self, *args):
		new_board_reality = self.imagine(*args)
		if type(new_board_reality) == int: return "something wrong in the imagination"
		word, coords, orientation = args
		self.wordspace.append([word, coords, orientation])
		for each in enumerate(self.lexicon):
			if each[1].upper().replace(' ','').startswith(word):
				self.history.append(self.lexicon.pop(each[0]))
				print(f"excised d'lexicon: {self.history[-1]}")
				break
		self.solution = new_board_reality
		fnordotron = self.inasraid
		if fnordotron:
			db.add_one_inasra_word_please(fnordotron, word, orientation, coords[0], coords[1])
		return

	def Start(self):
		is_context_cli = True # Hardcoded for now
		if is_context_cli:
			new_adventure = Whiptail()
			new_adventure.title = "inasra welcomes you"
			new_adventure.backtitle = lorem()
			word, exitstatus = new_adventure.inputbox('what shall you offer to inasra?')
			system("ps -ef|grep visualise | grep -v grep || xterm -e  './visualizations/bashvisualise.py'")
		else: pass # we were called by a web browser TODO

		inasraid = db.db_insert("inasra", name = word)
		choice_pos = 0

		# Chomp the starting word
		wikified_word = wikichompdb.wiki_query_prep(word)
		wikichompdb.wikipedia_grab_chomp(wikified_word)
		word_obj = self.db_word_obj(wikified_word)
		if word_obj is None:
			print(f'we tried real hard, but db_word_obj failz0red: {word}')

		# TODO: this needs to be converted to use the "inasra_spine" table instead
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

def load_test():
	with open('fartpuzzle.ipuz') as yet:
		return inasra(**json.loads(yet.read()))

def load_test_db():
	with open('fartpuzzle_db.ipuz') as yet:
		return inasra(**json.loads(yet.read()))

def main():
	with open('emptyinasra.ipuz') as fill: ths = inasra(**json.loads(fill.read()))
	ths.Start()

if __name__ == "__main__": main()
