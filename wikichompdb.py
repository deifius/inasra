#!/usr/bin/env python3

import wikipedia
import json
from sys import argv
import re
import pdb
from num2words import num2words
from whiptail import Whiptail
import db

# word = argv[1]
# if "/" in word: word = word.split('/')[-1]

def disambiguouizer(disambuchoices, ambiguous_word):
	whippyGUI = Whiptail()
	whippyGUI.title = "You've found the disambiguouizer"
	whippyGUI.backtitle = ambiguous_word + " may refer to;\n"
	user_choice, exitstatus = whippyGUI.menu(msg='what do you mean by ' +ambiguous_word+"?",items=disambuchoices,prefix='')
	return user_choice

def wiki_query_prep(word_or_phrase):
    ''' Hola pass me any string and I'll format it as a wikipedia article title.
        so "legislative chamber" becomes "Legislative_chamber"'''
    if ' ' in word_or_phrase:
        words = word_or_phrase.split(' ')
        wiki_article = words[0].capitalize() + "_" + '_'.join(words[1:])
        return wiki_article
    else: return word_or_phrase.capitalize()

def make_word_xword(wrd):
	numbers = re.compile('[0-9]')
	if len(numbers.findall(wrd)) > 0:
		for numba in re.findall('[0-9]+', wrd):
			wrd = re.sub(numba, num2words(numba, to="year"), wrd)
	return wrd

def wikipedia_grab_chomp(wikiterm):
	'''I retrieve linked articles, summaries and picture locations from wikipedia
		I used to put the chomped wiki stuff in a dir, but now I put that junk in a sqlite3 db'''
	words = db.db_query("select * from word where word = ?", wikiterm)
	if len(words) < 1:
		try:
			#pdb.set_trace()
			autosuggestSetting = False
			page = wikipedia.page(wikiterm, None, autosuggestSetting)
		except wikipedia.DisambiguationError as disambu_choices:
			# TODO: handle non-CLI contexts here
			#print(f'DisambiguationError {wikiterm}')
			page = wikipedia.page(disambiguouizer(disambu_choices.options, wikiterm))

		# pdb.set_trace()
		wordid = db.db_insert("word", word = wikiterm, url = page.url, summary = page.summary, content = page.content)
		links = []
		for link in page.links:
			links.append(link.split('(')[0])
		#pattern = re.compile('[\W_]+')
		numbers = re.compile('[0-9]')
		goodwords = set(links)
		# badwords = []
		#pdb.set_trace()
		for wrd in list(goodwords):
			# if len(numbers.findall(wrd)) > 0:
			# 	# in: clue w/ #, out: same clue, no #
			# 	# for numba in re.findall('[0-9]+', wrd):
			# 	# 	goodwords.add(re.sub(numba, num2words(numba, to="year"), wrd))
			# 	# 	# goodwords = ['twenty five or 6 to 4', 'twenty five or six to 4', 'twenty five or six to four']

			goodword = make_word_xword(wrd)
			goodwords.add(goodword)
			if wrd != goodword: goodwords.remove(wrd)

			# for numba in re.findall('[0-9]+', wrd):
			# 	wrd = re.sub(numba, num2words(numba, to="year"), wrd)
			# goodwords.add(wrd) #'twenty five or six to four'

				#pdb.set_trace()
				#print("throwing out '" +e+ "': don't do numbers yet")
				#badwords.append(wrd)
				# badwords = ['4']
		# for e in badwords:
		# 	goodwords.remove(e)
		goodwords = list(goodwords)
		#pdb.set_trace()
		# with open('acronym/links/' + wikiterm, 'w') as links:
		# 	links.write(json.dumps(goodwords))

		for goodword in goodwords:
			linkid = db.db_insert("word_links", word_id = wordid, link = goodword)

		for image in page.images:
			linkid = db.db_insert("word_images", word_id = wordid, image_url = goodword)

		# with open('acronym/summary/' + wikiterm, 'w') as summary:
		# 	summary.write(json.dumps(page.summary))

			#db.db_insert("word_links",)
		# with open('acronym/summary/' + wikiterm, 'w') as summary:
		# 	summary.write(json.dumps(page.summary))
		# with open('acronym/images/' + wikiterm, 'w') as images:
		# 	images.write(json.dumps(page.images))
		# with open('acronym/content/' + wikiterm, 'w') as content:
		# 	content.write(json.dumps(page.content))


#inasrafieldtest = open(".eggspine.txt",'w')
#if __name__ == "__main__": wikipedia_grab_chomp(word)
