#!/usr/bin/env python3
import json
from pdb import set_trace
#from os import system
from sys import argv
#import subprocess
from glob import glob
from time import sleep
from os import system

# Yo I receive a coordinate in X Y format on the xwordspine board
# I construct a list of regular expressions for legal word configurations which intersect the coordinate provided
# I then compare the list to the freqygoodword list and return any matches
# a reference to a file in .NextMoves/ 

X = int(argv[1])
Y = int(argv[2])
print(str(X) + ',' + str(Y))
#set_trace()
# then a miracle happens, as described below😘️

for eachPossibleMove in glob('.NextMoves/*MTtable*'):
	with open(eachPossibleMove) as possiboard: MTclue = json.loads(possiboard.read())
	if MTclue[X][Y] != " ": 
		#for e in MTclue: print(" ".join(e))
		print(str(eachPossibleMove))
		

