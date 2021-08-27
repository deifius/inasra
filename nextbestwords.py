#!/usr/bin/env python3

import json
import os
import subprocess

# run me and I'll fill .NextMoves with as many possible board states with one tangentially relevant word
# not yet on the board.  I grab OneBigDict, which is a list sorted by relevancy and start with legal places
# the concepts most integral to the current board concept.

#I am designed to be interrupted, NextMovesThinker clears the mem and restarts me constantly.

with open('freqygoodwords.json') as ok: Relevants = json.loads(ok.read())
if len(Relevants)>80: Relevants = Relevants[0:36]
while Relevants:
	print(Relevants[0])
	subprocess.Popen(['python3', 'findnextwordspace.py', Relevants.pop()])
#for each in Places4BestWord:
#		#print(each)
#		subprocess.call(['python3', 'cluePLACER.py'] + each.split(' ') + ['&'])
#		subprocess.Popen(['python3', 'clueonMTtable.py'] + each.split(' ') + ['&'])
