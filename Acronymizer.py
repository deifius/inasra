#!/usr/bin/env python3

from sys import argv
import json
from random import shuffle
import os
import pdb
import db
from subprocess import check_output
import whiptail

'''	Input:
		first argument
		sbsequent arguments: the dictionary
	./Acronymizer.py $1    $(cat acronym/links/$1)'''

def get_relephant(wikiword):
	word_links = db.db_query('''
		SELECT wl.link
		FROM word_links wl
		INNER JOIN word w ON wl.word_id = w.id
		WHERE w.word = ?
	''', wikiword)
	relephant = []
	for word_link in word_links:
		relephant.append(word_link["link"])
	return relephant

def acronymize(wikiword, relephant):
	''' I accept a word and a list of related words and return
	    a relevant acronym of the word using only related words'''

	wikiword = wikiword.replace('_', ' ')

	acronym = []
	def initialyze(singleletter, relephant):
		if len(singleletter) != 1: return "only one letter plz"
		if singleletter.isspace(): return " "
		if singleletter == '_': return " "
		shuffle(relephant)
		for each in relephant:
			if each[0].capitalize() == singleletter.capitalize():
				return each
		return "##QWANTZ no match; increase relephant pool" # singleletter
	for eachletter in wikiword:
		#pdb.set_trace()
		acronym.append(initialyze(eachletter, relephant))
	return acronym

def get_choice_with_whiptail(word, acronym_words, relephant):
	#pdb.set_trace()
	# print('acronym_words')
	# for acronym_word in acronym_words: print(acronym_word)
	while ' ' in acronym_words: acronym_words.remove(' ')
	word = word.replace(' ', '')
	for each in enumerate(acronym_words):
		if each[1].isspace(): acronym_words[each[0]] = ('');
		else: acronym_words[each[0]] = str(each[0]) + "    " + word[each[0]] + "    " + each[1]
	thechoice = whiptail.Whiptail()
	thechoice.title = word
	thechoice.backtitle = 'inasra'
	possible_choices = acronym_words
	possible_choices.append('respin')
	choice_word, exitstatus = thechoice.menu('choose your path', possible_choices,'-')
	if exitstatus == '1':
		return -1
	if choice_word == "respin":
		# input("respinnin'")
		return get_choice_with_whiptail(word, acronym_words, relephant)
	#input("you said " + choice_word.split('    ')[-1])
	#input(choice_word.split('    ')[0])
	choice_pos = int(choice_word.split('    ')[0])
	return choice_pos

def do_acronomize(wikiterm):
	relephants = db.db_query('''
		SELECT wl.link
		FROM word_links wl
		INNER JOIN word w ON wl.word_id = w.id
		WHERE w.word = ?
	''', wikiterm)

	wordclean = wikiterm.replace('_', ' ')

	# relephant_words = [relephant_words for relephant in relephants]
	relephant_words = [r.link for r in relephants]
	# relephant_words = []
	# for relephant in relephants:
	# 	relephant_words.append(relephant.link)

	# acronymize(wordclean, acronym, relephant)
	return acronymize(wordclean, relephants)



def main():
	'''this bit allows us to handle either a word or a path'''
	if len(argv) != 2: word = " ".join(argv)
	else:
		word = argv[1]
		print(argv[1] + '\n')

	if "/" in word: word = word.split('/')[-1]

	related_words = do_acronomize(word)

	# '''this is where we pull from the sqlite3 db if it exists'''

	# maybe?
	# word = word.replace('_', ' ')
	#
	# relephant = db.db_query('''
	# 	SELECT wl.link
	# 	FROM word_links wl
	# 	INNER JOIN word w ON wl.word_id = w.id
	# 	WHERE w.word = ?
	# ''', word)
	#
	# # word = word.replace('_', ' ')
	# # word = word.replace('_', ' ')
	#
	# related_words = acronymize(word, db.db_query('''
	# 	SELECT wl.link
	# 	FROM word_links wl
	# 	INNER JOIN word w ON wl.word_id = w.id
	# 	WHERE w.word = ?
	# ''', relephant[0].)) # relephant here?

	# FIXME: the 2nd related_words needs to a relephant
	# respin will be broken until this is fixed
	choice_pos = get_choice_with_whiptail(word, related_words, related_words)

	# word = word.replace('_', ' ')
	# acronym = acronymize(word, relephant)
	#choice_pos = get_choice_with_whiptail(word, related_words, relephant)
	#choice_word = acronym[choice_pos].split('    ')[-1]
	#input("my choice word is: " + choice_word)
	#print(relephant)

	record_acronym_choice(word, choice_pos, choice_word, argv[1])
	#pdb.set_trace()
	os.system('./recursive_spine_builder.sh ' + argv[1] +'/'+ choice_word.replace(' ','_').split('/')[-1])

if __name__ == "__main__":    main()
