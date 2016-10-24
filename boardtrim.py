#!/usr/bin/env python3

import json

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
        print('')


board =json.loads(open("xwordspine.json").read())
boardtrim(board)
board = list(zip(*board))
boardtrim(board)
writio = open('xwordspine.json', 'w')
writio.write(json.dumps(board).replace('.',' '))
writio.close()

