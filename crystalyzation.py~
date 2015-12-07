#!/usr/bin/env python
import json
import re
import pdb

this =json.loads(open("xwordspine.json").read())

def boardtrim(this):
    destroy = 1
    for each in this[-1]:
        if each is ' ':
            pass
        else:
            destroy = 0
    if destroy == 1:
        this.pop(-1)
        boardtrim(this)
    elif destroy == 0:
        print('trimmed')


boardtrim(this)
this = list(zip(*this))
for each in this:
    each = list(each)
boardtrim(this)
this = list(zip(*this))
for each in range(len(this)):
    this[each] = list(this[each])

for each in this: print(each)

#place 1 horizontal
wordbones = []
for each_square in this[0]:
    wordbones.append(each_square.replace(' ','.'))
for each_square in range(len(this[1])):
    if this[1][each_square] is not ' ':  
        print(wordbones[each_square])
        wordbones[each_square] = this[0][each_square]
print(''.join(wordbones))
mystery_word = re.compile(''.join(wordbones))
pdb.set_trace()

#place -1 horizontal

