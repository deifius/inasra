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

# Take a triple-tuple of characters, return one character with either:
# - Empty string: this letter can be anything
# - "|": this letter is a hard block (no valid matches)
# - "x": the specified letter must match exactly
def condenseComparisonTriplet(triplet):
    # If neighbor lines contain a letter, return a hard stop
    if(triplet[1] == "" and (triplet[0] != "" or triplet[2] != "")):
        return "|"
    else:
        return triplet[1]

def buildComparisonLine(wordspace, x, y, wordAxis):
    neighborIndexes = getNeighborIndexes(wordspace, x, y, wordAxis)
    getAxisLine = axisVal(
        wordAxis,
        lambda n : getLine(wordspace, n, y, offAxis(wordAxis)),
        lambda n : getLine(wordspace, x, n, offAxis(wordAxis))
    )
    comparisonLines = reduce(
        lambda lines, idx : lines + (getAxisLine(idx),),
        neighborIndexes,
        ()
    )
    lineLen = len(comparisonLines[0])
    # Pad an empty row if we are on an edge
    if(len(neighborIndexes) == 2):
        emptyLine = ("",) * lineLen
        if(neighborIndexes[0] == 0): comparisonLines = (emptyLine,)    + comparisonLines
        else:                        comparisonLines = comparisonLines + (emptyLine,)
    # Final tuple-line, each being empty (safe), a char (hard match), or "|" (no match)
    getCharacterTriplet = lambda n : tuple(map(lambda line : line[n], comparisonLines))
    return reduce(
        lambda final, n : final + (condenseComparisonTriplet(getCharacterTriplet(n)),),
        range(lineLen),
        ()
    )

# Return array of valid regexes for a specific x/y and its word axis
# TODO
def getRegexesForLetter(wordspace, x, y, wordAxis):
    #neighborIndexes = getNeighborIndexes(wordspace, x, y, wordAxis)
    comparisonLine = buildComparisonLine(wordspace, x, y, wordAxis)
    pivotIndex = offAxisVal(wordAxis, x, y)
    print('evaluating at pivot'+str(pivotIndex), comparisonLine)
    # FIXME: This isn't correct
    # baseStrs = filter((
    #     comparisonLine[:pivotIndex],
    #     comparisonLine[pivotIndex+1:],
    # ))
    regexes = ()
    return regexes
    #if(pivotIndex < len(comparisonLine)-1):
        # regexes = reduce(
        #     tuple(range(pivotIndex)),
        #     regexes
        # )
