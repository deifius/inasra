#!/usr/bin/env python3

def rotateboard(board):
	return [list(row) for row in list(zip(*board))]



class wordboard: #
    def __init__(self, state):
        self.state = []
        self.dimensions = [len(state), len(state[0])] #the dimensions of the rectangle
        self.history = [] # the list of operations that have led to the current board state
        self.wordspace = [] # a list of relevant words ordered by relevance
    def resize(self): pass # sets dimensions of board
    def trim(self): pass # reduces board to minimal rectangle
    def rotate(self): pass # swaps horizontal and vertical faux_regex_lines
    def rotate(self): # swaps horizontal and vertical faux_regex_lines
        return [list(row) for row in list(zip(*board))]
    def findplaceword(self, word): pass # returns potential boardstates which include word
    def findfillspace(self, coordinates): pass # returns boardstates with a new word

    @vertical
        def vertical_operation(board):
            rotateboard(board)

    def do_vertical(func):
        def wrapper_do_vertial():
            rotateboard()
            func()
            rotateboard()
        return wrapper_do_vertical
