#!/usr/bin/env python3

import json
from time import sleep
from os import system
from glob import glob as golb


def showit():
	readio = json.loads(open('xwordspine.json', 'r').read())
	for e in readio: print(' '.join(e))

def lookatthemoves():
	for each in golb('.NextMoves/*'):
		with open(each) as pants: board = json.loads(pants.read())
		for e in board: print(' '.join(e))
		sleep(.4)
		system('clear')


while True:
	showit()
	sleep(.5)
	system('clear')

