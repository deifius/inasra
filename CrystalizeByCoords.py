#!/usr/bin/env python3
import json, re
from pdb import set_trace
from sys import argv
from glob import glob

description = '''
 Yo I receive a coordinate in X Y format on the xwordspine board
I construct a list of regular expressions for legal word
configurations which intersect the coordinate provided
I then compare the list to the freqygoodword list
and return any matches
'''

def rotate(board):
    #print(f"Rotating board:\n{board}")
    rotated = [list(row) for row in list(zip(*board))]
    #print(f"Rotated board:\n{rotated}")
    return rotated

def show_cross(zoard, position):
    #print(f"Original board:\n{zoard}")
    #print(f"Position to analyze: {position}")
    board = list(map(list, zoard))
    for each_line in board:
        each_line.append(' ')
        each_line.insert(0, ' ')
    board.insert(0, [' '] * len(board[0]))
    board.append([' '] * len(board[0]))
    position = [position[0] + 1, position[1] + 1]
    #print(f"Adjusted board for edge handling:\n{board}")
    
    for row in enumerate(board):
        for col in enumerate(row[1]):
            if abs(col[0] - position[0]) > 1:
                if abs(row[0] - position[1]) > 1:
                    board[col[0]][row[0]] = '%'
            if abs(row[0] - position[1]) == 0:
                if board[col[0]][row[0]] == ' ':
                    board[col[0]][row[0]] = '.'
            if abs(col[0] - position[0]) == 0:
                if board[col[0]][row[0]] == ' ':
                    board[col[0]][row[0]] = '.'
                if abs(row[0] - position[1]) == 0:
                    board[col[0]][row[0]] = '*'
    #print(f"Processed board with focus at position:\n{board}")
    return board

def get2planes(zoard, position):
    #print(f"Getting planes for position: {position}")
    board = show_cross(zoard, position)
    position = [position[0] + 1, position[1] + 1]
    horiz = rotate(board[position[0] - 1:position[0] + 2])
    board = rotate(board)
    vert = rotate(board[position[1] - 1:position[1] + 2])
    #print(f"Vertical plane:\n{vert}\nHorizontal plane:\n{horiz}")
    return vert, horiz

def check_for_viability(regex):
    #print(f"Checking viability of regex: {regex}")
    checkAlpha = re.compile('[a-zA-Z]')
    checkAster = re.compile('\*')
    if checkAlpha.findall(regex) and checkAster.findall(regex):
        #print("Regex is Viable for this crossword!")
        return True
    #print('Not viable regex for this board')
    return False

def return_max_regex(boardlet):
    #print(f"Starting return_max_regex with boardlet:\n{boardlet}")
    for e in enumerate(boardlet):
        if e[1][1] == "*": 
            #print(f"Breaking loop due to '*' at position {e[0]}")
            break
        if e[1][0].isalnum():
            if not e[1][1].isalnum():
                boardlet[e[0]][1] = '+'
        if e[1][2].isalnum():
            if not e[1][1].isalnum():
                boardlet[e[0]][1] = '+'
    boardlet.reverse()
    #print(f"Boardlet after first pass:\n{boardlet}")
    
    for e in enumerate(boardlet):
        if e[1][1] == "*": 
            print(f"Breaking loop due to '*' at position {e[0]}")
            break
        if e[1][0].isalnum():
            if not e[1][1].isalnum():
                boardlet[e[0]][1] = '+'
        if e[1][2].isalnum():
            if not e[1][1].isalnum():
                boardlet[e[0]][1] = '+'
    boardlet.reverse()
    #print(f"Boardlet after second pass:\n{boardlet}")
   
    boardlet = rotate(boardlet)[1]
    while '+' in boardlet:
        if boardlet.index('+') > boardlet.index('*'):
            boardlet = boardlet[:boardlet.index('+')]
        else:
            boardlet = boardlet[boardlet.index('+') + 1:]
    regboards = [''.join(boardlet)]
    #print(f"Initial regex pattern: {regboards}")
    
    if check_for_viability(regboards[0]) is False:
        return []
    
    while len(regboards[-1]) > 1:
        new_regex = regboards[-1][1:] if regboards[-1][0] == '.' else regboards[-1][2:]
        if check_for_viability(new_regex) is False:
            return regboards
        for each in range(len(new_regex)):
            if check_for_viability(new_regex[:each * -1]) is True:
                if new_regex[each * -1].isalpha():
                    print(f"Skipping regex with alpha ending: {new_regex[each * -1]}")
                else:
                    regboards.append(new_regex[:each * -1])
        regboards.append(new_regex)
        #print(f"Updated regex patterns: {regboards}")
    return regboards

def will_word_fit(word, regboards):
	"""	If the word fits in one
		of the regboard slots,
		I'll tell you which ones"""
	which_ones = []
	for each_slot in regboards:
		this_slot = re.compile(each_slot.replace('*','.')+"$")
		if this_slot.match(word.upper().replace(' ','')):
			which_ones.append(each_slot)
	return which_ones


def compare_freqy_to_regboards(freqy, regboards):
	good_places = []
	for each_word in freqy:
		where_it_fits = will_word_fit(each_word, regboards)
		if where_it_fits:
			good_places.append((each_word, where_it_fits))
		if len(good_places) > 100:
			return good_places
	return good_places
	"""	The way this really needs to work is
		is individual calls should compare a
		cardinal freqy good
	"""

	'''	Actually this regex
		match is running
		pretty fucking fast
	'''

def calculate_possible_words(ipuz_data, lexicon, row, col):
    print(f"Calculating possible words for adjusted position: (row={row}, col={col})")
    
    # Retrieve the solution grid
    solution = ipuz_data['solution']
    grid_height = len(solution)
    grid_width = len(solution[0])
    #print(f'solution=')
    #for e in solution: print(e)
    #print(f'grid_height,grid_width={grid_height,grid_width}')

    # Ensure the coordinates are within grid bounds
    if not (0 <= row < grid_height and 0 <= col < grid_width):
        print(f"Coordinates (row={row}, col={col}) are out of grid bounds.")
        return []

    #print(f"Fetching vertical and horizontal planes...")
    vert, horiz = get2planes(solution, [row, col])
    #print(f"Vertical plane: {vert}")
    #print(f"Horizontal plane: {horiz}")

    vert_regexes = return_max_regex(vert)
    horiz_regexes = return_max_regex(horiz)
    #print(f"Vertical regexes: {vert_regexes}")
    #print(f"Horizontal regexes: {horiz_regexes}")
    
    regexes = vert_regexes + horiz_regexes
    possible_words = compare_freqy_to_regboards(lexicon, regexes)
    
    print(f"Possible words found: {possible_words}")
    return possible_words

