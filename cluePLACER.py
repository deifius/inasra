#!/usr/bin/env python3
import json, re
from os import system
from pdb import set_trace
from sys import argv

Job = '''
feed me :
    a partially constructed crossword puzzle in a 2d array (ipuz)
    & a word you want to place on the board,
    & the valid location for the first letter of the word x,y,
    only then will cluePLACER return the puzzle with the clue inserted
    zip* the board to do down!!
'''

def loadargs():
    try:
        alexicon = argv[1]
        position = [int(argv[2]), int(argv[3])]
        orientation = argv[4] if len(argv) > 4 else 'horiz'
        if len(argv) > 5:
            board = json.loads(argv[5])['solution']
        else:
            with open("xwordspine.json") as readio:
                board = json.load(readio)
    except Exception as e:
        print(Job)
        print(f"Error: {e}")
        exit()  # Exit to prevent using undefined variables
    for e in board: print(e)
    return alexicon, board, position, orientation

def sanitize(alexicon, board, position):
    if len(alexicon) > len(board[0]) - position[1]:
        print("too long, submit shorter word")
        exit()
    if re.search("[^a-zA-Z ]", alexicon) is None:
        alexicon = ''.join(alexicon.lower().split(' '))
        return alexicon.upper().replace(' ', ''), board, position
    else:
        print("remove offending characters, submit l8ter")
        exit()

def insert(alexicon, board, position):
    regexalexicon = re.compile(''.join(board[position[0]][position[1]:position[1] + len(alexicon)]).replace(' ', '.'))
    if regexalexicon.match(alexicon) is None:
        #set_trace()
        print('\tnot fit')
        return 0
    for letter in alexicon:
        board[position[0]][position[1]] = letter
        position[1] = position[1] + 1
    return board

def main():
    alexicon, board, position, orientation = loadargs()
    print(f'orientation: {orientation}')
    if orientation == 'vert':
        board = [list(row) for row in zip(*board)]
    sanitized_alexicon, board, position = sanitize(alexicon, board, position)
    updated_board = insert(sanitized_alexicon, board, position)
    #set_trace()
    if orientation == 'vert':
        updated_board = [list(row) for row in zip(*updated_board)]
    print(json.dumps(updated_board))
    #with open(f'.NextMoves/{sanitized_alexicon}.{orientation}.{position[0]}.{position[1]}', 'w') as writio:
    #    writio.write(json.dumps(updated_board))

if __name__ == "__main__":
    main()

