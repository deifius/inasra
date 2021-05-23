#!/usr/bin/env python3

from sys import argv
import json
from random import shuffle
import os
import pdb


#	Input:
#		first argument
#		sbsequent arguments: the dictionary
#	./Acronymizer.py $1  $(cat acronym/links/$1)


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

def get_choice(word, acronym, relephant):
	#pdb.set_trace()
	while ' ' in acronym: acronym.remove(' ')
	word = word.replace(' ','')
	for each in enumerate(acronym):
		if each[1].isspace(): print('');
		else: print(str(each[0]) +".\t"+ word[each[0]] +"\t"+ each[1])
	choice_word = input("\nSelect a line by number:\t")
	print("you said "+choice_word)
	if choice_word.isspace() or len(choice_word) == 0:
		pdb.set_trace()
		acronymize(word, acronym, relephant)
		#pdb.set_trace()
		choice_word = get_choice(word, acronym, relephant)
		return choice_word
		#os.system('./ye_Olde_init.sh ' + argv[1])
	try:		choice_word = int(choice_word)
	except:	get_choice(word, acronym, relephant)
	return choice_word

def main():
	if len(argv) != 2: word = " ".join(argv)
	else:
		word = argv[1]
		print(argv[1] + '\n')

	if "/" in word: word = word.split('/')[-1]

	with open('acronym/links/'+word) as ok: relephant = json.loads(ok.read())

	word = word.replace('_', ' ')
	acronym = []

	acronymize(word, acronym, relephant)
	choice_word = get_choice(word, acronym, relephant)
	print(acronym[int(choice_word)].replace(' ','_'))
	#print(relephant)

	with open('.eggspine.txt','a+') as inasradna:
		#pdb.set_trace()
		inasradna.write(word +"\t"+ str(choice_word) + "\n")
		print("I just wrote " + word)
	os.system('python3 spinylize.py; echo "Acronymizer line 70"; python3 boardtrim.py')
	userdir = 'users/$USER/'+ argv[1];
	newdir = userdir +'/'+ acronym[int(choice_word)].replace(' ','_').split('/')[-1]
	os.system('mkdir -p ' + newdir)
	#os.system('python3 xword2html.py xwordspine.json > ' + newdir + '/xword.html')
	os.system('cp acronym/links/' + word.replace(' ','_') + " " + userdir + "/links.json")
	os.system('cp acronym/images/' + word.replace(' ','_') + " " + userdir + "/images.json")
	os.system('cp acronym/summary/' + word.replace(' ','_') + " " + userdir + "/summary.json")
	os.system('cp acronym/content/' + word.replace(' ','_') + " " + userdir + "/content.json")
	os.system('python3 xword2jsonhtml.py xwordspine.json ' + userdir + ' > ' + newdir + '/xword.json.html')


	#pdb.set_trace()
	os.system('./ye_Olde_init.sh ' + argv[1] +'/'+ acronym[int(choice_word)].replace(' ','_').split('/')[-1])

if __name__ == "__main__":  main()
