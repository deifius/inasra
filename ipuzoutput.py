#!/usr/bin/env python3

import ipuz
import json

class xword_:
	dimensions =  {width = 0, height = 0}
## Dimensions of the puzzle grid
	puzzle =  []
## The puzzle rows, then columns
	solution =  []
#Correct solution	

basic_format = '''
{{
    "version": "http://ipuz.org/v2",
    "kind": [ "http://ipuz.org/crossword#1" ],
    "dimensions": { "width": 3, "height": 3 },
    "puzzle": [ [ { "cell": 1, "style": { "shapebg": "circle" } }, 2, "#" ],
                [ 3, { "style": { "shapebg": "circle" } }, 4 ],
                [ null, 5, { "style": { "shapebg": "circle" } } ] ],
    "solution": [ [ "C", "A", "#" ],
                  [ "B", "O", "T" ],
                  [ null, "L", "O" ] ],
    "clues": { "Across": [ [ 1, "OR neighbor" ],
                           [ 3, "Droid" ],
                           [ 5, "Behold!" ] ],
               "Down": [ [ 1, "Trucker's radio" ],
                            [ 2, "MSN competitor" ],
                            [ 4, "A preposition" ] ] }
}
'''
