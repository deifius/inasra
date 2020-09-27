#!/bin/bash

# I create a directory of the best next possible moves, based on the strongest elements of OneBigDict
# OneBigDict is sorted so that the 0th element is the least frequently linked 

[ -d ".NextMoves/" ] && rm .NextMoves/* > /dev/null; 
[ ! -d ".NextMoves/" ]	&& mkdir .NextMoves && echo "YES" # && sudo mount -t tmpfs -o size=1024m tmpfs .NextMoves

if test -f ".wordplacementideal"; then rm .wordplacementideal; fi
python3 nextbestwords.py


#for goodwordidea in $( head -n 60 .nextbestwords.log ); do
#	#echo "$goodwordidea"
#	python3 crystalyzation.py $goodwordidea >> .wordplacementideal; done


# this is the same as the commented-out loop above, reading through by line
#while IFS= read -r -u13 line; do 
#   python3 cluePLACER.py $line >> .wordplacementideal; done 13<".wordplacementideal"

#for e in $(ls .NextMoves/*.png); do echo "$e"; sleep .5; done

# the following line produces a random image from the NextMoves folder:
#expressions=($(ls .NextMoves/*.png)) && echo ${expressions[$RANDOM % ${#expressions[@]} ]}
