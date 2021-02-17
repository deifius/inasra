#!/usr/bin/env python3

import wikipedia
import json
from sys import argv
import re
import pdb


word = argv[1]
if "/" in word: word = word.split('/')[-1]

def disambiguouizer(disambuchoices, ambiguous_word):
	print(ambiguous_word + " may refer to;\n")
	for each in enumerate(disambuchoices):
		print(str(each[0]) + ":", each[1])
	userchoice = -1
	while 0 >  userchoice or userchoice > len(disambuchoices):
		userchoice = int(input('you choose(0-' + str(len(disambuchoices)) + '): \t'))
	return str(disambuchoices[userchoice])
	


def wikipedia_grab_chomp(wikiterm):
	'''I retrieve linked articles, summaries and picture locations from wikipedia'''
	
	try:
		page = wikipedia.page(wikiterm)
	except wikipedia.DisambiguationError as disambu_choices:
		#pdb.set_trace()
		page = wikipedia.page(disambiguouizer(disambu_choices.options, word))
	
	links = []
	for link in page.links:
		links.append(link.split('(')[0])
	pattern = re.compile('[\W_]+')
	numbers = re.compile('[0-9]')
	goodwords = set(links)
	badwords = []
	#pdb.set_trace()
	for e in goodwords:
		if len(numbers.findall(e)) > 0:
			print("throwing out '" +e+ "': don't do numbers yet")
			badwords.append(e)
	for e in badwords:
		goodwords.remove(e)
	goodwords = list(goodwords)
	#pdb.set_trace()
	with open('acronym/links/' + wikiterm, 'w') as links:
		links.write(json.dumps(goodwords))
	with open('acronym/summary/' + wikiterm, 'w') as summary:
		summary.write(json.dumps(page.summary))
	with open('acronym/images/' + wikiterm, 'w') as images:
		images.write(json.dumps(page.images))
	with open('acronym/content/' + wikiterm, 'w') as content:
		content.write(json.dumps(page.content))

wikipedia_grab_chomp(word)
