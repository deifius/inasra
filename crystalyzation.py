#!/usr/bin/env python
import json
import re
import pdb
from glob import glob as glob

board =json.loads(open("xwordspine.json").read())

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

def boardprint(board):
    for each in board: print(each)

#place 1 horizontal
wordbones = []
for each_square in board[0]:
    wordbones.append(each_square.replace(' ','\S'))
for each_square in range(len(board[1])):
    if board[1][each_square] is not ' ':  
        #print(wordbones[each_square])
        wordbones[each_square] = board[0][each_square]
killer = "".join(wordbones)
mystery_word = re.compile(killer)

sumpin = glob('acro_dicts/*.json')
biglexicon = []
for each in sumpin:
    once = json.loads(open(each).read())
    for every in once:
        for each in every:
            each = re.sub('[^a-z]','',each)
            biglexicon.append(each.replace(' ',''))
lines = []
def findnextwordspace (board):
    for space in range(len(board[0])):
        if  board[0][space] == ' ' and board[1][space] == ' ':
            board[0][space] = '.'
    for space in range(len(board[-1])):
        if  board[-1][space] == ' ' and board[-2][space] == ' ':
            board[-1][space] = '.'
    for eachline in range(len(board)):
        for space in range(len(board[0])):
            if board[eachline][space] == ' ':
                if board[eachline-1][space] == '.' or board[eachline-1][space] == ' ':
                    if board[eachline+1][space] == '.' or board[eachline+1][space] == ' ':
                        board[eachline][space] = '.'
    for each in board:
        lines.append(''.join(each))
    obstacle = re.compile('\.?[a-z][a-z]+\.?')
    for i in range(len(lines)):  
        lines[i] = re.sub(obstacle,'',lines[i],)
        if re.search('[a-z| ]',lines[i],) is None:
            lines[i] = '<empty>'
        if re.search('\.',lines[i],) is None:
            lines[i] = '<empty>'

    for i in range(len(lines)):
        if lines[i] == '<empty>': continue
        start = 0
        end = 0
        templist = list(lines[i])
        while templist[0] == '.':
            templist.pop(0)
            start = start + 1
        while templist[-1] == '.':
            templist.pop(-1)
            end = end + 1
        lines[i] = '.{,' + str(start) + '}' + ''.join(templist) + '.{,' + str(end) + '}'
    newentries = []
    for i in range(len(lines)):
        for j in range(len(biglexicon)):
            if re.match(lines[i], biglexicon[j]) is not None:
                newentries.append([i, biglexicon[j]])
    pdb.set_trace()

findnextwordspace(board)
pdb.set_trace()
#  lol I can search biglexicon for well formulated regex strings from the board

writio = open('xwordspine.json', 'w')
writio.write(json.dumps(board))
writio.close()
#place -1 horizontal
