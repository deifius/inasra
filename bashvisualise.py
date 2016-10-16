#!/usr/bin/env python

import json
from time import sleep
from os import system


def showit():
    readio = json.loads(open('xwordspine.json', 'r').read())
    for e in readio: print(' '.join(e))

while True:
    showit()
    sleep(.5)
    system('clear')
