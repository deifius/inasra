#!/usr/bin/env python3

import wikipedia
import json
import sys
import re
import pdb

def wikipedia_grab_chomp(wikiterm):
	'''I retrieve linked articles, summaries and picture locations from wikipedia'''
	page = wikipedia.page(wikiterm)
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
			print("throwing out '" +e+ "' because we don't do numbers yet")
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

wikipedia_grab_chomp(sys.argv[1])
