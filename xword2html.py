#!/usr/bin/env python3

from tabulate import tabulate
import json

#Hallo I generate an html with buttons for letters to std
#input xwordspine.json
with open('xwordspine.json') as ok: this = json.loads(ok.read())

for each in enumerate(this):
    for every in enumerate(each[1]):
            if every[1] != ' ':
                    this[each[0]][every[0]] = '<button type="button">'+every[1]+"</button>"

print(tabulate(this, tablefmt='html'))
