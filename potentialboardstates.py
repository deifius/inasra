#!/usr/bin/env python3

import json


with open('OneBigDict.json') as ok: Relevants = json.loads(ok.read())
while Relevants:
	print(Relevants.pop())


