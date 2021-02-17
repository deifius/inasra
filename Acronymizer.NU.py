#!/bin/env python3

from sys import argv
import json
from random import shuffle
import os
import pdb

#	Input: 
#		first argument 
#		sbsequent arguments: the dictionary 
#	./Acronymizer.NU.py $1  $(cat acronym/links/$1)

word = argv[1]
if "/" in word: word = word.split('/')[-1]
with open('acronym/links/'+word) as ok: relephant = json.loads(ok.read())
word = word.replace('_', ' ')


acronym = []

print(word)
def acronymize(word, acronym, relephant):
	'''I accept a string and return a relevant acronym'''
	def initialyze(singleletter, relephant):
		if len(singleletter) != 1: return "only one letter plz"
		if singleletter.isspace(): return " "
		shuffle(relephant)
		for each in relephant:
			if each[0].capitalize() == singleletter.capitalize():
				return each
		return singleletter #"##QWANTZ no match; increase relephant pool"
	for eachletter in word:
		#pdb.set_trace()
		acronym.append(initialyze(eachletter, relephant))

acronymize(word, acronym, relephant)
for each in enumerate(acronym): 
	if each[1].isspace(): print(''); 
	else: print(str(each[0]) +".\t"+ word[each[0]] +"\t"+ each[1])

next_word = input("Select a line by number:\t")
print(acronym[int(next_word)].replace(' ','_'))
#print(relephant)
