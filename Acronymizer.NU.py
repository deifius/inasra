#!/usr/bin/env python3

from sys import argv
import json
from random import shuffle
import os
import pdb


#	Input:
#		first argument
#		sbsequent arguments: the dictionary
#	./Acronymizer.NU.py $1  $(cat acronym/links/$1)

if len(argv) != 2: word = input("\n\n\nwhat do you want to make an acronym for? ")
else:
	word = argv[1]
	print(argv[1] + '\n')

if "/" in word: word = word.split('/')[-1]

with open('acronym/links/'+word) as ok: relephant = json.loads(ok.read())

word = word.replace('_', ' ')
acronym = []

def acronymize(word, acronym, relephant):
	'''I accept a string and return a relevant acronym'''
	def initialyze(singleletter, relephant):
		if len(singleletter) != 1: return "only one letter plz"
		if singleletter.isspace(): return " "
		shuffle(relephant)
		for each in relephant:
			if each[0].capitalize() == singleletter.capitalize():
				return each
		return "##QWANTZ no match; increase relephant pool" # singleletter
	for eachletter in word:
		#pdb.set_trace()
		acronym.append(initialyze(eachletter, relephant))

def get_choice(word, acronym):
	#pdb.set_trace()
	for each in enumerate(acronym):
		if each[1].isspace(): print('');
		else: print(str(each[0]) +".\t"+ word[each[0]] +"\t"+ each[1])
	choice_word = input("\nSelect a line by number:\t")
	print("you said "+choice_word)
	if choice_word.isspace() or len(choice_word) == 0:
		#acronymize(word, acronym, relephant)
		choice_word = get_choice(word, acronym)
		#os.system('./ye_Olde_init.sh ' + argv[1])
	try:		choice_word = int(choice_word)
	except:	get_choice(word, acronym)
	return choice_word

acronymize(word, acronym, relephant)
choice_word = get_choice(word, acronym)
print(acronym[int(choice_word)].replace(' ','_'))
#print(relephant)

with open('.eggspine.txt','a') as inasradna: inasradna.write(word +"\t"+ str(choice_word) +"\n")
os.system('./ye_Olde_init.sh ' + argv[1] +'/'+ acronym[int(choice_word)].replace(' ','_'))
