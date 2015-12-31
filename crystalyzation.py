#!/usr/bin/env python
import json
import re
import pdb
from glob import glob as glob
import random
import socket

board = json.loads(open("xwordspine.json").read())

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

boardtrim(board)
board = list(zip(*board))
for each in board:
    each = list(each)
boardtrim(board)
board = list(zip(*board))
for each in range(len(board)):
    board[each] = list(board[each])

depants = open('visualyze3d/thepants.txt','w')
for each in range(len(board)):
	for space in range(len(board[each])):
		if board[each][space] == ' ':
			print('ok')
		else:
			goods = board[each][space]+' 0 '+str(each)+' '+str(space)+';\n'
			depants.write(goods)
depants.close()

pdb.set_trace()
#place 1 horizontal
wordbones = []
for each_square in board[0]:
    wordbones.append(each_square.replace(' ', '.'))
for each_square in range(len(board[1])):
    if board[1][each_square] is not ' ':
        print(wordbones[each_square])
        wordbones[each_square] = board[0][each_square]
print(''.join(wordbones))
mystery_word = re.compile(''.join(wordbones))


acroglob = glob('acro_dicts/*')
maybe_bone = []
for each in acroglob:
    maybe_bone.append(json.loads(open(each).read()))

flat_list_of_maybe_bones = []
for each in maybe_bone:
    for every in each:
        for single in every:
            flat_list_of_maybe_bones.append(single)
random.shuffle(flat_list_of_maybe_bones)

pdb.set_trace()
#Why are my for loops broken?



#place -1 horizontal

