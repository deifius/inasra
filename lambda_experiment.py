from functools import reduce

def getLetterAtPos(x, y, wordspace, axis):
    return wordspace[x][y]
#    if axis == 'x': return wordspace[x][y]
#    else:           return wordspace[y][x]

def getColumn(wordspace, n):
    return list(map(lambda word : word[n], wordspace))

def flipWordspace(wordspace):
    enumeratedFirstWord = enumerate(wordspace[0])
    return list(map(lambda pos : getColumn(wordspace, pos[0]), enumeratedFirstWord))

def getRow(x, y, wordspace, wordAxis):
    letter = getLetterAtPos(x, y, wordspace, wordAxis)
    if   wordAxis == 'x': return flipWordspace(wordspace)[y]
    elif wordAxis == 'y': return wordspace[x]

def getRegexesForLetter(x, y, wordspace, wordAxis):
    row = getRow(x, y, wordspace, wordAxis)
    rowReverse = row[::-1]
    #backLetters = reduce(lambda out, x : out + x + x, row, '')
    #return backLetters

thing = [['h', 'i'], [' ', 'f']]

print('hi')
print(getColumn(thing, 1))
print(flipWordspace(thing))
print(getRow(0, 1, thing, 'y')) # hi
print(getRow(0, 1, thing, 'x')) # if
#print(getRegexesForLetter(0, 1, thing, 'x')) # if
