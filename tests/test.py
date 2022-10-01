import os
import unittest
import sys
import re
import inspect
import json
from functools import reduce

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import Start_New_inasra
from legacy import lambda_experiment as ws
import findnextwordspace

with open("tests/testspine.json") as readio:
	testspine = json.loads(readio.read())

class TestStringMethods(unittest.TestCase):

	def test_rotateboard(self):
		testboard = [['a', 'b'], ['c', 'd']]
		rotato = findnextwordspace.rotateboard(testboard)
		self.assertEqual(rotato, [['a', 'c'], ['b', 'd']])

	def test_sanitize(self):
		taco = findnextwordspace.sanitize(testspine, 'ta co')
		nah = findnextwordspace.sanitize(testspine, 'n_a_h')
		self.assertEqual(taco, 'taco')
		self.assertEqual(nah, None)

	def test_generate_faux_regex_lines(self):
		# print("+ " * len(testspine[0]) + "+ +")
		# for each_line in testspine:
		# 	print(f"+ {' '.join(each_line)} +")
		# print("+ " * len(testspine[0]) + "+ +")
		lines = findnextwordspace.generate_faux_regex_lines(testspine)
		self.assertEqual(lines[0][0], 'S')
		self.assertEqual(lines[1], 'i.................................')
		self.assertEqual(lines[3], 'AdaptationSofSherlockHolmes.......')
		self.assertEqual(lines[5], 't.........e.......................')

	def test_identify_legalplace(self):
		lines = findnextwordspace.generate_faux_regex_lines(testspine)
		legalplaces_list = findnextwordspace.identify_legalplace(lines, 'taco')
		legit_x, legit_y = legalplaces_list[0]
		self.assertEqual(legit_x, 5)
		self.assertEqual(legit_y, 0)
		self.assertEqual(len(legalplaces_list), 8)
		self.assertEqual(legalplaces_list, [(5, 0), (8, 7), (9, 8), (12, 7), (17, 9), (23, 22), (27, 7), (30, 7)])

	def test_findnextwordspace_vert(self):
		# lines = findnextwordspace.generate_faux_regex_lines(testspine)
		# print(lines)
		# FIXME: why dafuq is testspine changing in memory
		with open("tests/testspine.json") as readio:
			deffresh = json.loads(readio.read())
		#

		print("+ " * len(deffresh[0]) + "+ +")
		for each_line in deffresh:
			print(f"+ {' '.join(each_line)} +")
		print("+ " * len(deffresh[0]) + "+ +")

		rotato = findnextwordspace.rotateboard(deffresh)
		print("+ " * len(rotato[0]) + "+ +")
		for each_line in rotato:
			print(f"+ {' '.join(each_line)} +")
		print("+ " * len(rotato[0]) + "+ +")
		vert = findnextwordspace.findnextwordspace(rotato, 'taco')
		for item in vert: print(item)
		self.assertEqual(vert, [(2, 2), (4, 3), (5, 2), (6, 3), (8, 0), (14, 20), (15, 21), (17, 18), (18, 0), (19, 1), (21, 20), (22, 0), (32, 19)])

	def test_upper(self):
		self.assertEqual('foo'.upper(), 'FOO')

	def test_isupper(self):
		self.assertTrue('FOO'.isupper())
		self.assertFalse('Foo'.isupper())

	def test_createdirs(self):
		Start_New_inasra.directory_initializer()
		self.assertTrue(os.path.isdir('acronym/summary'))
		self.assertFalse(os.path.isdir('i/am/not/a/dir'))

	def test_split(self):
		s = 'hello world'
		self.assertEqual(s.split(), ['hello', 'world'])
		# check that s.split fails when the separator is not a string
		with self.assertRaises(TypeError):
			s.split(2)

	def test_col(self):
		wordspace = (('h', 'i'), (' ', 'f'))
		self.assertEqual(ws.getColumn(wordspace, 1), ('i', 'f'))
		self.assertEqual(ws.flipWordspace(wordspace), (('h', ' '), ('i', 'f')))
		self.assertEqual(ws.offAxis('y'), 'x')
		self.assertEqual(ws.offAxisVal('y', 5, 10), 5)

	def test_wordspace(self):
		wordspace = (
			('h', 'o', 'w'),
			('e', '' , '' ),
			('f', '' , '' ),
			('t', '' , '' ),
		)
		self.assertEqual(ws.getWordspaceLen(wordspace, 'x'), 3)
		self.assertEqual(ws.getWordspaceLen(wordspace, 'y'), 4)

		self.assertEqual(ws.getLine(wordspace, 0, 2, 'y'), ('h', 'e', 'f', 't')) #f
		self.assertEqual(ws.getLine(wordspace, 1, 0, 'x'), ('h', 'o', 'w'))	  #o

		self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 0, 'y'), (0, 1))	#h
		self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 2, 'y'), (1, 2, 3)) #f
		self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 3, 'y'), (2, 3))	#t
		self.assertEqual(ws.getNeighborIndexes(wordspace, 0, 0, 'x'), (0, 1))	#h
		self.assertEqual(ws.getNeighborIndexes(wordspace, 2, 0, 'x'), (1, 2))	#w

		self.assertEqual(ws.condenseComparisonTriplet(('a', '', '')), '|')
		self.assertEqual(ws.condenseComparisonTriplet(('', '', 'a')), '|')
		self.assertEqual(ws.condenseComparisonTriplet(('', 'a', '')), 'a')
		self.assertEqual(ws.condenseComparisonTriplet(('', '', '')), '')

		self.assertEqual(ws.buildComparisonLine(wordspace, 1, 0, 'x'), ('o', '|', '|', '|'))
		self.assertEqual(ws.buildComparisonLine(wordspace, 2, 0, 'x'), ('w', '',  '',  '' ))
		self.assertEqual(ws.buildComparisonLine(wordspace, 0, 1, 'y'), ('e', '|', '|'))
		self.assertEqual(ws.buildComparisonLine(wordspace, 0, 3, 'y'), ('t', '',  '' ))

		wordspace2 = wordspace + (('y', 'e', 's'),)
		self.assertEqual(ws.buildComparisonLine(wordspace2, 1, 0, 'x'), ('o', '|', '|', '|', 'e'))
		self.assertEqual(ws.buildComparisonLine(wordspace2, 2, 0, 'x'), ('w', '',  '',  '',  's'))

		rgxstr = '[\[\]\(\),]'
		self.assertEqual(re.sub(rgxstr, '', '[h(el)lo,]'), 'hello')

		# TODO: Import this function
		alexicon = 'the'
		legalplace = [(10, 15), (16, 2)]
		goodplaces = tuple(map(
			lambda item:
				alexicon
				+ ' '
				+ ' '.join(list(map(lambda s : str(s), item))),
			legalplace
		))
		self.assertEqual(goodplaces, ('the 10 15', 'the 16 2'))

		#expectedRegexes = ('p.{1,2}')
		# self.assertEqual(ws.getRegexesForLetter(wordspace, 2, 0, 'x'), expectedRegexes)
		# self.assertEqual(ws.getRegexesForLetter(wordspace, 0, 2, 'y'), expectedRegexes)

if __name__ == '__main__':
	unittest.main()
