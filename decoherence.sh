#!/bin/bash

# TODO: make this an independent function, rip it out of wikichomp
#  user choice limits: 0 only on first word.  1 only available if -1(last index) previous choice
#  catch more input- reroll the acronym and display current xword spine interface options
#  integrate hyperlinks into the acro_dicts so fewer errors and ambiguousities are thrown
#  improve rerolling options - gui last item selection, present clue potential
#  ken.burns specfx for background

# I accept the argument: 1 item from the .NextMoves/ directory
# and I make it into the the next actual board state
# we are creating the directory hierarchy for spannable history trees,
echo $1|grep -q PlacedClue
if [ $? = 0 ]
then
	echo "$1"
	test -f $1
	if [ $? = 0 ]
	then
		echo "should be doin now"
		echo "$inasradir"
		#mkdir -p $inasradir/$1/.NextMoves
		mv $1 xwordspine.json
		#mv .NextMoves/* $inasradir/.NextMoves
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
