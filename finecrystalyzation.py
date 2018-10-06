#!/usr/bin/env python3
import json
import re
import pdb
import random
from os import system

board =json.loads(open("xwordspine.json").read())

alexicon = json.loads(open('OneBigDict.json').read())

def findnextwordspace (board):
	lines = []
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
		for j in range(len(alexicon)):
			if re.match(lines[i], alexicon[j]) is not None:
				entry = []
				entry.append(i)
				entry.extend(list(alexicon[j]))
				newentries.append(entry)
	random.shuffle(newentries) #main diff with crystalization
	chosen_one = ''
	while chosen_one is '':
		chosen_line = int(newentries[-1].pop(0))
		chosen_word = newentries.pop()
		alignment = []
		for x in range(len(board[chosen_line])):
			if re.match('[^\.]',board[chosen_line][x]) is not None:
				#pdb.set_trace()
				alignment.append([x,board[chosen_line][x]])
		while alignment[0][1] is not chosen_word[alignment[0][0]]:
			chosen_word = ['.'] + chosen_word
			if len(chosen_word) > len(board[chosen_line]): break

		if len(chosen_word) < len(board[chosen_line]):
			for e in range(len(chosen_word)):
				board[chosen_line][e] = chosen_word[e]
				chosen_one = chosen_word

#  lol I can search alexicon for well formulated regex strings from the board
def visualize(xwordfield):
	system('clear')
	print('')
	for eachline in xwordfield:
		line = ' '
		linecheck = 0
		for each in eachline:
			line = line + ' ' + each
			if each != ' ':
				linecheck = 1
		if linecheck == 1:
			print(line)

wegotwords = ''
while wegotwords == '':
	try:
		findnextwordspace(board)
		visualize(board)
		board = list(zip(*board))
	except:
		wegotwords = 'no we do not'


vvisualize(board)
board = list(zip(*board))
with open('xwordspine.json', 'w') as writeio:
	writeio.write(json.dumps(board).replace('.',' '))

#place -1 horizontal
