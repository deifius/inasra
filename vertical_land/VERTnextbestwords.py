#!/usr/bin/env python3

import json
import os
import subprocess

# run me and I'll fill .NextMoves with as many possible board states with one tangentially relevant word
# not yet on the board.  I grab freqygoodwords, which is a list sorted by relevancy and start with legal places
# the concepts most integral to the current board concept.

#I am designed to be interrupted, NextMovesThinker clears the mem and restarts me constantly.  

with open('../freqygoodwords.json') as ok: Relevants = json.loads(ok.read())
Relevants = Relevants[0:30]
while Relevants:
	Places4BestWord = json.loads(subprocess.check_output(['python3', 'crystalyzationvert.py', Relevants.pop()]))
	for each in Places4BestWord:
		print(each)
		subprocess.call(['python3', 'cluePLACERvert.py'] + each.split(' ') + ['&'])
		subprocess.Popen(['python3', 'clueonMTtablevert.py'] + each.split(' ') + ['&'])
