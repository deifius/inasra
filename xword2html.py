#!/usr/bin/env python3

# DEPRECATED: we now use xword2jsonhtml.py

from tabulate import tabulate
import json, re
from sys import argv

#Hallo I generate an html with buttons for letters to std
#input xwordspine.json
#this = argv[1]
with open(argv[1]) as ok: this = json.loads(ok.read())
#with open('xwordspine.json') as ok: this = json.loads(ok.read())

#for each in enumerate(this):
#    for every in enumerate(each[1]):
#            if every[1] != ' ':
#                    this[each[0]][every[0]] = "<button type='button'>"+every[1]+"</button>"




header = '''
<!DOCTYPE html>
<html>
<body>

<script>
function siblingCount(node) {
	return [...node.parentElement.childNodes].indexOf(node);
}

function klik(btn) {
	const x = siblingCount(btn.parentElement.parentElement);
	const y = siblingCount(btn.parentElement);
	document.location = `/cluez/lukifer/usufruct?action=click&x=${x}&y=${y}`;
}
</script>

<h2>INASRA</h2>
'''
footer = '</html>\n</body>'

#with open('xword.html','w') as writor:
#	writor.write(header)
#	writor.write(tabulate(this, tablefmt='html'))
#	writor.write(footer)

print(header)
#print(tabulate(this, tablefmt='html'))
print(re.sub('>([\S\s])<', r'><button onclick="klik(this)">\1</button><',tabulate(this, tablefmt='html')))

print(footer)
