#!/bin/env python3

from sys import argv
import json
from random import shuffle
import pdb

word = argv[1]
#with open('acronym/links/'+ word, 'r') as relephants:
#	relephant = json.loads(relephants.read())
#	relephant.sort()
relephant = json.loads(''.join(argv[2:]))	

#	Input: 
#		first argument 
#		sbsequent arguments: the dictionary 
acronym = []
def acronymize(word, acronym, relephant):
	'''I accept a string and return a relevant acronym'''
	def initialyze(singleletter, relephant):
		if len(singleletter) != 1: return "only one letter plz"
		if singleletter == ' ': return ' '
		shuffle(relephant)
		for each in relephant:
			if each[0].capitalize() == singleletter.capitalize():
				return each
		return "##QWANTZ no match; increase relephant pool"
	
	for eachletter in word:
		acronym.append(initialyze(eachletter, relephant))


acronymize(argv[1], acronym, relephant)
for each in enumerate(acronym): print(word[each[0]] + "\t" + each[1])


#pdb.set_trace()
#print(relephant)
