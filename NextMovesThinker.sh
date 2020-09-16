#!/bin/bash

# I create a directory of the best next possible moves, based on the strongest elements of OneBigDict
#

[ -d ".NextMoves/" ] && rm .NextMoves/* > /dev/null; 
[ ! -d ".NextMoves/" ]	&& mkdir .NextMoves && echo "YES" # && mount -t tmpfs -o size=1024m tmpfs NextMoves; fi

if test -f ".wordplacementideal"; then rm .wordplacementideal; fi
python3 nextbestwords.py > .nextbestwords.log


for goodwordidea in $( head -n 60 .nextbestwords.log ); do
	#echo "$goodwordidea"
	python3 crystalyzation.py $goodwordidea >> .wordplacementideal; done


# this is the same as the commented-out loop above, reading through by line
while IFS= read -r -u13 line; do 
   python3 cluePLACER.py $line >> .wordplacementideal; done 13<".wordplacementideal"


