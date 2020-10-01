#!/usr/bin/env python

import json
import pdb



def boardtrim(board):
    destroy = 1
    for each in board[-1]:
        if each is ' ':
            pass
        else:
            destroy = 0
    if destroy == 1:
        board.pop(-1)
        boardtrim(board)
    elif destroy == 0:
        print('trimmed')
boardspine = json.loads(open("../xwordspine.json").read())
letterquantity = len(boardspine) * len(boardspine[0])
boardtrim(boardspine)
board = list(zip(*boardspine))
for each in boardspine:
    each = list(each)
boardtrim(board)
boardspine = list(zip(*boardspine))
for each in range(len(boardspine)):
    boardspine[each] = list(boardspine[each])
boardtrim(boardspine)
field = []
for every in range(letterquantity):
	posy = str(100 + every%len(boardspine) * 25)
	posx = str(100 + every%len(boardspine[0]) * 80)
	field.append("#X obj "+ posx +" " + posy + " letter " + str(every+1) + ";\n")
letterfield = open('letterarray.pd','w')
letterfield.write('#N canvas 1 52 450 300 10;\n')
for pdobj in field:
	letterfield.write(pdobj)
letterfield.close()