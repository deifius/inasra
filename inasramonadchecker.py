#!/usr/bin/env python3

from sys import argv
import json

'''This guy receives a json striing
& verifies if it is an inasra monad
'''
def monad_tests(isit_json):
    try:    isit_inasra = json.loads(isit_json)
    except:
        print("submit one json string please")
        return -1
    if len(isit_inasra) < 2 or type(isit_inasra[0]) != list:
        print("need 2 args, 0: dimensions, 1: the word")
        print("element 0 must be a list describing the position of the word")
        return 1
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
        print('needed: 1d list of contiguous space to fit word')
        return 4
    print(isit_inasra[1] + " is inasra")

if __name__ == "__main__": monad_tests(argv[1])
