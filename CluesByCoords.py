#!/usr/bin/env python3
import json
import re
from pdb import set_trace
#from os import system
from sys import argv
#import subprocess

# Yo I receive a coordinate in X Y format on the xwordspine board
# I construct a list of regular expressions for legal word configurations which intersect the coordinate provided
# I then compare the list to the freqygoodword list and return any matches
# in the format of a... list of fully constructed board states including the new word 


with open("xwordspine.json") as readio: board =json.loads(readio.read())
coords = [int(argv[1]), int(argv[2])]
print(coords)
#set_trace()
print(board[coords[0]][coords[0]])
# then a miracle happens!
