#!/usr/env python3


#TODO rather than port this whole thing to python3 and then break it down, trim this to pure wikichomp function and then port that to python 3.  recursor and decoheresy are coded directly in py3
import re
import sys
import random
import urllib.request
import string
import json
import pdb
import subprocess
from time import sleep
from os import system
import pdb

#linkable words that are part of wikipedia boilerplate
wiki_words_reserved = json.loads(open('wiki_reserve_terms.json').read())
#pdb.set_trace()
#TODO: develop a kickass regex (and a bloom filter) which encompasses many variations of reserved words!
#

inasrafieldtest = open("inasrafieldtest.txt",'w')

def disambiguouizer(ambiguous_wiki, ambiguous_term):
	#in the event of an amiguous term, the disambiguouizer lets user select the proper meaning
	refertochomp = ambiguous_wiki.find(b'may refer to') + 18
	endchomp = ambiguous_wiki.find(b"disambigbox") - 11
	disambuslice = re.findall(b'a href=".+">.+<.+>, .+</li>\n', ambiguous_wiki[refertochomp:endchomp])
	disambuchoices =[]
	#print(endchomp)
	for each in disambuslice:
		targt = each.split(b'"')[1]
		descr = each.split(b',')[1].split(b'<')[0]
		title = each.split(b'"')[3]
		disambuchoices.append([title, descr,targt])
	print(ambiguous_term + " may refer to;\n")
	selection = 0
	for each in disambuchoices:
		print(selection, each[0].decode() + ":", each[1].decode())
		selection+= 1
	userchoice = -1
	while 0 >  userchoice or userchoice > selection:
		userchoice = int(input('you choose(0-' + str(selection) + '): \t'))
	ambiguous_term = disambuchoices[userchoice][2].split(b'/')[-1]
	acronymizer(str(ambiguous_term)[2:-1])

def acronymizer(wikitarget):
	if '(' in wikitarget:
		properly_capped = wikitarget.split('(')[0].replace(' ', '_').title() \
									+"("+ wikitarget.split('(')[1]
		wikitarget = wikitarget.split('(')[0]
	else:
		properly_capped = wikitarget.replace(' ', '_').title()
	properly_capped = properly_capped.replace('&','%26')
	####print("http://en.wikipedia.org/wiki/" + properly_capped + "\n\n")
	req = urllib.request.Request("http://en.wikipedia.org/wiki/" + properly_capped)#, \
				#headers={'User-Agent': 'Mozilla/5.0 (Fuck You Wikipedia; Me; emdash)'})
	wiki_dump = urllib.request.urlopen(req).read().lower()
	#pdb.set_trace()
	#print(wiki_dump)
	if wiki_dump.count(b'isambiguation') > 10:
		#10 seems to be more instances of 'disambiguous' references than non disambiarticales contain
		disambiguouizer(wiki_dump, wikitarget)
	relevance_regex = re.compile('<a href="/wiki/.*?" title=".*?">.*?</a>')
	relephants = re.findall(relevance_regex, str(wiki_dump))
	inasrafieldtest.write(wikitarget + '\t')
	#construct vocabulary which contains lists of relevant terms for every letter of the acronymed word
	vocabulary = []
	#here
	wikiwords = re.compile('('+')|('.join(wiki_words_reserved)+')')
	for each in relephants:
		questionable_content = re.sub(".*>","",each[:-4])
		#pdb.set_trace()
		if wikiwords.match(questionable_content) is None:
			vocabulary.append(questionable_content) 
	for bang in range(0,vocabulary.count('')):
		vocabulary.remove('')
	vocab = sorted(vocabulary, key=str.lower)
	#form a dictionary from vocabulary
	acro_term = wikitarget.lower().translate(str.maketrans("","")) #got from http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
	acronym_dict = []
	for element in acro_term:
		if element == '_' or element == ' ':
			acronym_dict.append('')
			continue
		acronym_equiv = []
		for each in vocab:
			if each[0] == element:
				acronym_equiv.append(each)
		acronym_dict.append(acronym_equiv)

## A regex to excise all reserved wikiwords will be needed here.  It should be its own function and 
	for element in wiki_words_reserved:
		for letter_dict in acronym_dict:
			while element in letter_dict:
				letter_dict.remove(element)
	for tick in range(len(acronym_dict)):
		if acronym_dict[tick] == []:
			acronym_dict[tick].append(acro_term[tick])
	
	print(acro_term + " acronymized:")
	acro_records = open("acro_dicts/" + acro_term + ".json", 'w')
	acro_records.write(json.dumps(vocabulary))
	acro_records.close()
#TODO: this is what will become decoheresy
	running_acronym = []
	selection = 0
	# now generate a random acronym from the dictionary
	# && recursify
	userchoice = -1
	print("\n" + acro_term + " acronymized!")
	#pdb.set_trace()
	while 0 >  userchoice or userchoice > selection:
		for each in acronym_dict:
			if each in ['','.']:
				print(each)
			else:
				running_acronym.append(random.choice(each))
				print(str(selection) + ".\t" + running_acronym[-1][0].title() + " \t" + running_acronym[-1].capitalize())
				selection+= 1
		userchoice = input('you choose(0-' + str(selection-1) + '): \t')
		if userchoice == '':
			inasrafieldtest.flush()
			exec(compile(open('spinylize.py','rb').read(), 'spinylize.py', 'exec'))
			userchoice = -1
			selection = 0
			print("+-+-+-+-+-+-+-+-+-+\n")
		userchoice = int(userchoice)
	inasrafieldtest.write(str(userchoice) + '\n')
	term = running_acronym[userchoice]
		#for each in acronym_dict:
	#	if each == '':
	#		print
	#	else:
	#		print(random.choice(each))
	acronymizer(term)


if len(sys.argv) != 2:
	term = input("\n\n\nwhat do you want to make an acronym for? ")
else:
	term = sys.argv[1]
acronymizer(term)
