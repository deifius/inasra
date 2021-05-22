#!/bin/bash

#  user choice limits: 0 only on first word.  1 only available if -1(last index) previous choice
#  catch more input- reroll the acronym and display current xword spine interface options
#  integrate hyperlinks into the acro_dicts so fewer errors and ambiguousities are thrown
#  improve rerolling options - gui last item selection, present clue potential
#  ken.burns specfx for background

# I accept the argument: 1 item from the .NextMoves/ directory
# and I make it into the the next actual board state
# we are creating the directory hierarchy for spannable history trees,
inasradir=$(python3 -c "print('$2'.strip())")
newcrystal=$(python3 -c "print('$1'.split('/')[-1][0:])")
echo $1|grep -q PlacedClue
if [ $? = 0 ]
then
	echo "$1"
	test -f $1
	if [ $? = 0 ]
	then
		echo "should be doin now"
		echo "$inasradir$newcrystal"
		mkdir -p $inasradir$newcrystal
		mv $1 xwordspine.json
		cp xwordspine.json $inasradir$newcrystal
		rm .NextMoves/*
		echo $1 >> .eggspine.txt
		python3 freqyforget.py $1
		python3 nextbestwords.py
	else
		echo "dont see it in .NextMoves"
	fi
else
	echo "gimme a PlacedClue"
fi
