#!/usr/env python

import re
import sys
import random
import urllib2
import string

#linkable words that are part of wikipedia boilerplate
wiki_words_reserved = ['isbn','random article','help','issn','related changes','recent changes','info','all articles with unsourced statements','Community portal','Main page','Special pages','Removed','Cite','Disclaimers','Upload file']

wiki_words_reserved = ['isbn','random article','help','issn','related changes','recent changes','info','all articles with unsourced statements']

#TODO: develop a kickass regex which encompasses many variations of reserved words!

def disambiguouizer(ambiguous_wiki, ambiguous_term):
	refertochomp = ambiguous_wiki.find('may refer to') + 18
	endchomp = ambiguous_wiki.find('<tr>\n<td class="mbox-image"')
	disambuslice = re.findall('title=".+">.+<.+>, .+</li>\n', ambiguous_wiki[refertochomp:endchomp])
	disambuchoices =[]
	print ambiguous_wiki[refertochomp:endchomp]
	#print disambuslice
	for each in disambuslice:
		descr = each.split(',')[1].split('<')[0]
		title = each.split('"')[1]
		disambuchoices.append([title, descr])
	print ambiguous_term + " may refer to;\n"
	selection = 0
	for each in disambuchoices:
		print str(selection) + ". " + each[0] + ", " + each[1]
		selection+= 1
	userchoice = -1
	while 0 >  userchoice or userchoice > selection:
		userchoice = int(input('you choose(0-' + str(selection) + '): \t'))
	ambiguous_term = disambuchoices[userchoice][0]
	acronymizer(ambiguous_term)

def acronymizer(wikitarget):
	req = urllib2.Request("http://en.wikipedia.org/wiki/%s" % wikitarget.replace(' ', '_').title(), \
		              headers={'User-Agent': 'Mozilla/5.0 (Fuck You Wikipedia; Me; emdash)'})
	print wikitarget.replace(' ', '_').title()
	wiki_dump = urllib2.urlopen(req).read().lower()
	if wiki_dump.count('isambiguation') > 5:
		disambiguouizer(wiki_dump, wikitarget)
	relevance_regex = re.compile('<a href="/wiki/.*?" title=".*?">.*?</a>')
	relephants = re.findall(relevance_regex,wiki_dump)

	#construct vocabulary
	vocabulary = []
	for each in relephants:
		vocabulary.append(re.sub(".*>","",each[:-4])) 
	for bang in range(0,vocabulary.count('')):
		vocabulary.remove('')
	vocab = sorted(vocabulary, key=str.lower)

	#form a dictionary from vocabulary
	acro_term = wikitarget.lower().translate(string.maketrans("",""), string.punctuation) #got from http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
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


	for element in wiki_words_reserved:
		#print "looking for '" + element + "' to remove"
		for letter_dict in acronym_dict:
			while element in letter_dict:
				letter_dict.remove(element)
				#print "removed!"
	for tick in range(len(acronym_dict)):
	    if acronym_dict[tick] == []:
		acronym_dict[tick].append(acro_term[tick])
	# now generate a random acronym from the dictionary
	# && recursify
	print acro_term + " acronymized:"
	running_acronym = []
	selection = 0
	#print acronym_dict
	for each in acronym_dict:
		if each in ['','.']:
			print each
		else:
			running_acronym.append(random.choice(each))
			print str(selection) + ".\t" + running_acronym[-1][0].title() + " \t" + running_acronym[-1].capitalize()
			selection+= 1
	userchoice = -1
	print "\n" + acro_term + " acronymized!"
	while 0 >  userchoice or userchoice > selection:
		userchoice = int(input('you choose(0-' + str(selection-1) + '): \t'))
	term = running_acronym[userchoice]
	#for each in acronym_dict:
	#	if each == '':
	#		print
	#	else:
	#		print random.choice(each)
	acronymizer(term)
if len(sys.argv) != 2:
	term = raw_input("what do you want to make an acronym for? ")
else:
	term = sys.argv[1]
acronymizer(term)
