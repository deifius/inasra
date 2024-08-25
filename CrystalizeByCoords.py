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
	return [list(row) for row in list(zip(*board))]

def show_cross(zoard, position):
	board = list(map(list, zoard))
	for each_line in board:
		each_line.append(' ')
		each_line.insert(0, ' ')
	board.insert(0, [' ']*len(board[0]))
	board.append([' ']*len(board[0]))
	position = [position[0]+1, position[1]+1]
	"""	Just adding temp rows and columns to line the board
		permitting searching at the edges, top & bottom"""
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
	for e in board[0]: e
	return board

def get2planes(zoard, position):
	'''i return two planes along the axes of the position'''
	board = show_cross(zoard, position)
	position = [position[0]+1, position[1]+1]
	horiz = rotate(board[position[0]-1:position[0]+2])
	board = rotate(board)
	vert = rotate(board[position[1]-1:position[1]+2])
	return vert, horiz

def check_for_viability(regex):
	checkAlpha = re.compile('[a-zA-Z]')
	checkAster = re.compile('\*')
	if checkAlpha.findall(regex) and checkAster.findall(regex):
		#print("Regex is Viable for this crossword!")
		return True
	#print('Not viable regex for this board')
	return False

def return_max_regex(boardlet):
	"""	feed me a height 3 board of any width
		I will feed back the longest eachPossible
		regex for the middle row of the boardlet
	"""
	for e in enumerate(boardlet):
		if e[1][1] == "*": break
		if e[1][0].isalnum():
			if not e[1][1].isalnum():
				boardlet[e[0]][1] = '+'
		if e[1][2].isalnum():
			if not e[1][1].isalnum():
				boardlet[e[0]][1] = '+'
	boardlet.reverse()
	for e in enumerate(boardlet):
		if e[1][1] == "*": break
		if e[1][0].isalnum():
			#print("letter on top")
			if not e[1][1].isalnum():
				#print(f"{'.'.join(e[1])}no letter inline: nonviable")
				boardlet[e[0]][1] = '+'
				#print(f'boardlet length:{len(boardlet)}')
		if e[1][2].isalnum():
			if not e[1][1].isalnum():
				boardlet[e[0]][1] = '+'
	boardlet.reverse()
	boardlet = rotate(boardlet)[1]
	while '+' in boardlet:
		if boardlet.index('+') > boardlet.index('*'):
			boardlet = boardlet[:boardlet.index('+')]
		else: boardlet = boardlet[boardlet.index('+')+1:]
	regboards =  [''.join(boardlet)] # longest possible regex in this place
	if check_for_viability(regboards[0]) is False:
		return [] # no viable moves on this axis
	while len(regboards[-1]) > 1:
		new_regex = regboards[-1][1:] if regboards[-1][0] == '.' else regboards[-1][2:]
		if check_for_viability(new_regex) is False:
			return regboards
		for each in range(len(new_regex)):
			if check_for_viability(new_regex[:each*-1]) is True:
				if not new_regex[each*-1].isalpha():
					regboards.append(new_regex[:each*-1])
				else: print(f"gotta skip it cuz last char was :{new_regex[each*-1]}")
		regboards.append(new_regex)
	return regboards

def get_freqy(inasra):
	try:
		if inasra.lexicon: freqy = inasra
		else: freqy = inasra.set_lexicon()
		return freqy
	except :
		print('failed to get freqy witchu')

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

def turn_match_to_board(position, good_place, orientation):
	word_prepped = good_place[0].upper().replace(' ','')
	if orientation == "vert": position = [position[0]-good_place[1][0].index('*'), position[1]]
	else: position = [position[0], position[1]-good_place[1][0].index('*')]
	return word_prepped, position[0], position[1]

def calculate_possible_words(ipuz_data, lexicon, x, y):
    # Retrieve the solution grid
    solution = ipuz_data['solution']
    
    # Get the vertical and horizontal planes for the given coordinates
    vert, horiz = get2planes(solution, [x, y])
    
    # Calculate the max regex patterns for both orientations
    vert_regexes = return_max_regex(vert)
    horiz_regexes = return_max_regex(horiz)
    
    # Combine both regex lists
    regexes = vert_regexes + horiz_regexes
    
    # Find good places in the puzzle for the words from the lexicon
    possible_words = compare_freqy_to_regboards(lexicon, regexes)
    
    return possible_words



def main():
	X,Y = int(argv[1]), int(argv[2])
	if len(argv) == 4:
		board = argv[-1]
	else:
		with open('xwordspine.json') as bookit:
				board = json.loads(bookit.read())
				if board[X][Y] != " ":
					print("got to handle this")
					exit(1)

"""
from CluesBeHere import *
import inasra; ya=inasra.load_test()
hyper = ya.set_lexicon()
newpos = [8,0]
vert, horiz = get2planes(ya.solution, newpos)
this, that = return_max_regex(horiz), return_max_regex(vert)
vick, huck = compare_freqy_to_regboards(hyper,that),compare_freqy_to_regboards(hyper,this)
turn_match_to_board(newpos, huck[30])
huck[30][0]
huck[30]
huck
turn_match_to_board(newpos, huck[0])
ya.add_word_horiz(*turn_match_to_board(newpos, huck[0]))
ya.show_solution()
newpos = [9,9]
vert, horiz = get2planes(ya.solution, newpos); this, that = return_max_regex(horiz), return_max_regex(vert); vick, huck = compare_freqy_to_regboards(hyper,that),compare_freqy_to_regboards(hyper,this)
for e in enumerate(huck): e
ya.add_word_horiz(*turn_match_to_board(newpos, huck[0]))
ya.show_solution()
newpos = [8,9]
vert, horiz = get2planes(ya.solution, newpos); this, that = return_max_regex(horiz), return_max_regex(vert); vick, huck = compare_freqy_to_regboards(hyper,that),compare_freqy_to_regboards(hyper,this)
for e in enumerate(vick): e
vick[1]
ya.add_word_vert('Steatorrhea',3,9)
ya.show_solution()
ya.add_word_vert('Steatorrhea',2,9)
ya.show_solution()
ya.add_word_vert('Steatorrhea'.upper(),2,9)
ya.show_solution()
ya.add_word_vert('Steatorrhea'.upper(),3,9)
ya.show_solution()
ya.add_word_vert(' Steatorrhea'.upper(),2,9)
ya.show_solution()
newpos = [8,11]
vert, horiz = get2planes(ya.solution, newpos); this, that = return_max_regex(horiz), return_max_regex(vert); vick, huck = compare_freqy_to_regboards(hyper,that),compare_freqy_to_regboards(hyper,this)
for e in enumerate(vick): e
ya.add_word_vert(' Graflex'.upper(),6,11)
ya.show_solution()
ya.add_word_vert(' Graflex'.upper(),5,11)
ya.show_solution()
newpos = [2,4]
vert, horiz = get2planes(ya.solution, newpos); this, that = return_max_regex(horiz), return_max_regex(vert); vick, huck = compare_freqy_to_regboards(hyper,that),compare_freqy_to_regboards(hyper,this)
for e in enumerate(vick): e
for e in enumerate(huck): e
huck[3]
turn_match_to_board(newpos, huck[3])
turn_match_to_board(newpos, huck[16])
turn_match_to_board(newpos, huck[19])
ya.add_word_horiz('puddlesign'.upper(),2,0)
ya.show_solution()
ya.add_word_horiz('buddleja     '.upper(),2,0)
ya.show_solution()
newpos = [3,7]
vert, horiz = get2planes(ya.solution, newpos); this, that = return_max_regex(horiz), return_max_regex(vert); vick, huck = compare_freqy_to_regboards(hyper,that),compare_freqy_to_regboards(hyper,this)
huck
vivk
vick
newpos = [5,7]
vert, horiz = get2planes(ya.solution, newpos); this, that = return_max_regex(horiz), return_max_regex(vert); vick, huck = compare_freqy_to_regboards(hyper,that),compare_freqy_to_regboards(hyper,this)
vick
huck
"""
if __name__ == '__main__': main()
