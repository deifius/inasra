#!/usr/bin/env python3

from sys import argv
import json
from random import shuffle
import os
import pdb
from subprocess import check_output
import whiptail

#	Input:
#		first argument
#		sbsequent arguments: the dictionary
#	./Acronymizer.py $1    $(cat acronym/links/$1)


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

def get_choice_with_whiptail(word, acronym, relephant):
	#pdb.set_trace()
	while ' ' in acronym: acronym.remove(' ')
	word = word.replace(' ','')
	for each in enumerate(acronym):
		if each[1].isspace(): acronym[each[0]] = ('');
		else: acronym[each[0]] = str(each[0]) + "    " + word[each[0]] + "    " + each[1]
	thechoice = whiptail.Whiptail()
	thechoice.title = word
	thechoice.backtitle = 'inasra'
	possible_choices = acronym
	possible_choices.append('respin')
	choice_word, exitstatus = thechoice.menu('choose your path', possible_choices,'-')
	if exitstatus == '1':
		return 0
	if choice_word == "respin":
		input("respinnin'")
		get_choice_with_whiptail(word, acronym, relephant)
	#input("you said " + choice_word.split('    ')[-1])
	#input(choice_word.split('    ')[0])
	choice_pos = int(choice_word.split('    ')[0])
	return choice_pos

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
	choice_pos = get_choice_with_whiptail(word, acronym, relephant)
	choice_word = acronym[choice_pos].split('    ')[-1]
	#input("my choice word is: " + choice_word)
	#print(relephant)

	with open('.eggspine.txt','a+') as inasradna:
		#pdb.set_trace()
		inasradna.write(word +"\t"+ str(choice_pos) + "\n")
		print("I just wrote " + word)
	os.system('python3 spinylize.py; echo "COnstruturing"; python3 boardtrim.py')
	userdir = 'users/$USER/'+ argv[1];
	newdir = userdir +'/'+ choice_word.replace(' ','_').split('/')[-1]
	#input('new dir is: ' + newdir)
	os.system('mkdir -p ' + newdir)
	#os.system('python3 xword2html.py xwordspine.json > ' + newdir + '/xword.html')
	os.system('cp acronym/links/' + word.replace(' ','_') + " " + userdir + "/links.json")
	os.system('cp acronym/images/' + word.replace(' ','_') + " " + userdir + "/images.json")
	os.system('cp acronym/summary/' + word.replace(' ','_') + " " + userdir + "/summary.json")
	os.system('cp acronym/content/' + word.replace(' ','_') + " " + userdir + "/content.json")
	os.system('python3 xword2jsonhtml.py xwordspine.json ' + userdir + ' > ' + newdir + '/xword.json.html')
	#pdb.set_trace()
	os.system('./recursive_spine_builder.sh ' + argv[1] +'/'+ choice_word.replace(' ','_').split('/')[-1])

if __name__ == "__main__":    main()
