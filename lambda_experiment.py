from functools import reduce

def offAxis(wordAxis):          return 'y' if wordAxis == 'x' else 'x'
def offAxisVal(wordAxis, x, y): return  y  if wordAxis == 'x' else  x
def    axisVal(wordAxis, x, y): return  x  if wordAxis == 'x' else  y

# Get the length of one side of a wordspace
def getWordspaceLen(wordspace, axis):
    if   axis == 'x': return len(wordspace[0])
    elif axis == 'y': return len(wordspace)

def getLetterAtPos(wordspace, x, y):
    return wordspace[x][y]

def getColumn(wordspace, n):
    return tuple(map(lambda word : word[n], wordspace))

def flipWordspace(wordspace):
    enumeratedFirstWord = enumerate(wordspace[0])
    return tuple(map(lambda pos : getColumn(wordspace, pos[0]), enumeratedFirstWord))

def getLine(wordspace, x, y, wordAxis):
    if   wordAxis == 'x': return wordspace[y]
    elif wordAxis == 'y': return flipWordspace(wordspace)[x]

# Get the x/y index for a specific row/col, and its next/prev neighbors if possible
def getNeighborIndexes(wordspace, x, y, wordAxis):
    maxPos = getWordspaceLen(wordspace, wordAxis) - 1
    wordIdx = axisVal(wordAxis, x, y)
    return tuple(filter(
        lambda pos : pos >= 0 and pos <= maxPos,
        (
            wordIdx - 1,
            wordIdx,
            wordIdx + 1,
        )
    ))

def getRegexesForLine(line, pos):
    lineStr = ''.join(line)
    maxPos = len(lineStr) - 1
    # temp
    return (lineStr+str(pos),)

# Return array of valid regexes for a specific x/y and its word axis
def getRegexesForLetter(wordspace, x, y, wordAxis):
    neighborIndexes = getNeighborIndexes(wordspace, x, y, wordAxis)
    pivotIndex = offAxisVal(wordAxis, x, y)
    getAxisLine = axisVal(
        wordAxis,
        lambda n : getLine(wordspace, n, y, offAxis(wordAxis)),
        lambda n : getLine(wordspace, x, n, offAxis(wordAxis))
    )
    return reduce(
        lambda rgxs, idx: rgxs + getRegexesForLine(getAxisLine(idx), pivotIndex),
        neighborIndexes,
        ()
    )
