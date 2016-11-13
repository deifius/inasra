import cgi

import re
import sys
import random
import urllib2
import string

#form = cgi.FieldStorage()
#if not form.has_key("input"):
#	print """Content-Type: text/html

#<html>
#<head>
#  <title>[[Wikipedia|Wikichomp]] Acronymizer</title>
#</head>
#<body>
#  <form action="/" method="get">
#    <div><input type="text" name="input" size="60"/></div>
#    <div><input type="submit" value="Acronymize Word or Phrase w/ Its Wikipedia Article!"/></div>
#  </form>
#</body>
#</html>
#"""
#	sys.exit()

#print 'Content-Type: text/plain'
#print ''

term = sys.argv[1]

#grab the page and chomp relevant terms

 http://en.wikipedia.org/w/index.php?title=Cure&action=edit
req = urllib2.Request("http://en.wikipedia.org/wiki/%s" % term.replace(' ', '_'), \
req = urllib2.Request("http://en.wikipedia.org/wiki/%s" % term.replace(' ', '_'), \
                      headers={'User-Agent': 'Mozilla/5.0 (Wikipedia is nice; Me; emdash)'})
wiki_dump = urllib2.urlopen(req).read().lower()
relevance_regex = re.compile('<a href="/wiki/.*?" title=".*?">.*?</a>')
relephants = re.findall(relevance_regex,wiki_dump)

#construct lexicon
lexicon = []

for each in relephants:
	lexicon.append(re.sub(".*>","",each[:-4])) 
for bang in range(0,lexicon.count('')):
	lexicon.remove('')
vocab = sorted(lexicon, key=str.lower)

print vocab
