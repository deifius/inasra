#!/bin/bash

# TODO: make this an independent function, rip it out of wikichomp
#  user choice limits: 0 only on first word.  1 only available if -1(last index) previous choice
#  catch more input- reroll the acronym and display current xword spine interface options
#  integrate hyperlinks into the acro_dicts so fewer errors and ambiguousities are thrown 
#  improve rerolling options - gui last item selection, present clue potential
#  ken.burns specfx for background

# I accept the argument: 1 item from the .NextMoves/ directory
# and I make it into the the next actual board state

if test -f .NextMoves/$1; then

subprocess.call(mv $1 xwordspine.json)
subprocess.call(mv $1 xwordspine.json)

python3 -c "
import json
with open('freqygoodwords.json') as BigDict:
	BigDict.write(json.loads(BigDict.remove($1.split('.'))))
"
fi
rm .NextMoves/*
echo $1 >> .eggspine.txt
