#!/usr/bin/env python3

import json

def boardtrim(board):
	destroy = 1
	for each in board[-1]:
		if each == ' ':
			pass
		else:
			destroy = 0
	if destroy == 1:
		board.pop(-1)
		boardtrim(board)
	elif destroy == 0:
		print('')
	return board

def write_it_down(board):
	with open('xwordspine.json', 'w') as writio:
		writio.write(json.dumps(board).replace('.',' '))


def main():
	board =json.loads(open("xwordspine.json").read())
	boardtrim(board)
	board = list(zip(*board))
	boardtrim(board)
	write_it_down(board)


if __name__ == '__main__': main()
