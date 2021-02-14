#!/usr/bin/env python3

import json

with open("../xwordspine.json") as readio: board =json.loads(readio.read())

board = list(zip(*board))

with open('jackvertical.json', 'w') as writio:
	writio.write(json.dumps(board))
