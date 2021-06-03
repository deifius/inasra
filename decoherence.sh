#!/bin/bash

#  tobedone: user choice limits: 0 only on first word.
#  1 only available if -1(last index) previous choice
#  catch more input- reroll the acronym and display
#  current xword spine interface options
#  integrate hyperlinks into the acro_dicts so
#  fewer errors and ambiguousities are thrown
#  improve rerolling options -
#  gui last item selection,
#  present clue potential
#  autoken.burns pan&scan for background

# I accept the argument: 1 item from the .NextMoves/ directory
# and I make it into the the next actual board state
# we are creating the directory hierarchy for spannable history trees,


ancillary_word=$(python3 -c "print('$1'.split('/')[-1][0:])")
inasradir=$(python3 -c "print('$2'.strip())")

echo Ancillary Word:  $ancillary_word
echo inasra directory:  $inasradir

if [ $? = 0 ]
then
	#echo "$1"
	test -f $1
	if [ $? = 0 ]
	then
		#echo "should be doin now"
		#echo "$inasradir$ancillary_word"
		mkdir -p $inasradir/
		mv $1 xwordspine.json
		cp xwordspine.json $inasradir/
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

echo $inasradir

sleep 1
while $( ps -ef | grep cluePLACER | wc -l ) > 1
do
	sleep 1
	echo "still plenty of new board states to splinylize"
done
./whiptailCrystalizer.sh $inasradir/
#./whiptailCrystalizer.sh $inasradir
