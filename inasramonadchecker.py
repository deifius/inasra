#!/usr/bin/env python3

from sys import argv
import json

'''What has 2 thumbs and
& verifies if a received json string
 is an inasra monad
'''

'''this script'''

# I threw the part about having thumbs in to throw you off

'''inasra monads are relative position + word'''

def monad_test(isit_json):
    try:    isit_inasra = json.loads(isit_json)
    except:
        print("submit one json string please")
        return -1
    if len(isit_inasra) < 2 or type(isit_inasra[0]) != list:
        print("need 2 args, 0: dimensions, 1: the word")
        print("element 0 must be a list describing the position of the word")
        return 1 #verify json tl structure is correct
    if type(isit_inasra[1]) != str or not isit_inasra[1].isalpha():
        print("arg 1 must be the word")
        return 5 # check word fitness
    nonfloatdimensions = []
    for dimension in isit_inasra[0]:
        if type(dimension) != int:
                nonfloatdimensions.append(dimension)
    if len(nonfloatdimensions) != 1:
        print("all dimensions but one must be integer indices")
        return 3
    if (type(nonfloatdimensions[0]) != list or
        len(nonfloatdimensions[0]) != len(isit_inasra[1]) or
        not (lambda l: sorted(l) == list(range(min(l), max(l)+1)))(nonfloatdimensions[0])):
        print('needed: 1d list of contiguous space; precisely fitted for word')
        return 4
    print(isit_inasra[1] + " is inasra")

if __name__ == "__main__": monad_tests(argv[1])
