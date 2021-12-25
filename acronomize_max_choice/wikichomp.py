#!/usr/bin/env python3

import wikipedia
import json
from sys import argv
import re
import pdb
from num2words import num2words
from whiptail import Whiptail
#import db

def disambiguouizer(disambuchoices, ambiguous_word):
	whippyGUI = Whiptail()
	whippyGUI.title = "You've found the disambiguouizer"
	whippyGUI.backtitle = ambiguous_word + " may refer to;\n"
	user_choice, exitstatus = whippyGUI.menu(msg='what do you mean by ' +ambiguous_word+"?",items=disambuchoices,prefix='')
	return user_choice



def wikipedia_grab_chomp(wikiterm):
	'''I retrieve linked articles, summaries and picture locations from wikipedia
		I used to put the chomped wiki stuff in a dir, but now I put that junk in a sqlite3 db'''
	words = ""
	if len(words) < 1:
		try:
			#pdb.set_trace()
			page = wikipedia.page(wikiterm)
		except wikipedia.DisambiguationError as disambu_choices:
			#pdb.set_trace()
			page = wikipedia.page(disambiguouizer(disambu_choices.options, word))

		#pdb.set_trace()
		print(len(words))
		#wordid = db.db_insert("word",word = wikiterm, url = page.url, summary = page.summary, content = page.content)
		links = []
		for link in page.links:
			links.append(link.split('(')[0])
		pattern = re.compile('[\W_]+')
		numbers = re.compile('[0-9]')
		goodwords = set(links)
		badwords = []
		#pdb.set_trace()
		for e in list(goodwords):
			if len(numbers.findall(e)) > 0:
				# in: clue w/ #, out: same clue, no #
				for numba in re.findall('[0-9]+', e):
					goodwords.add(re.sub(numba, num2words(numba, to="year"), e))
				#pdb.set_trace()
				#print("throwing out '" +e+ "': don't do numbers yet")
				badwords.append(e)
		for e in badwords:
			goodwords.remove(e)
		goodwords = list(goodwords)
		#pdb.set_trace()
		with open('../acronym/links/' + wikiterm, 'w') as links:
			links.write(json.dumps(goodwords))
			#db.db_insert("word_links",)
		with open('../acronym/summary/' + wikiterm, 'w') as summary:
			summary.write(json.dumps(page.summary))
		with open('../acronym/images/' + wikiterm, 'w') as images:
			images.write(json.dumps(page.images))
		with open('../acronym/content/' + wikiterm, 'w') as content:
			content.write(json.dumps(page.content))


#inasrafieldtest = open(".eggspine.txt",'w')
if __name__ == "__main__":
	word = argv[1]
	if "/" in word: word = word.split('/')[-1]
	wikipedia_grab_chomp(word)
