#!/bin/bash

# I create a directory of the best next possible moves, based on the strongest elements of OneBigDict
#

#mkdir NextMoves
#mount -t tmpfs -o size=1024m tmpfs NextMoves
if test -f ".wordplacementideal"; then rm .wordplacementideal; fi

python3 nextbestwords.py > .nextbestwords.log


for goodwordidea in $( head .nextbestwords.log )
do
	#echo "$goodwordidea"
	python3 crystalyzation.py $goodwordidea >> .wordplacementideal
done

#for goodplace in $( head .wordplacementideal )
#do
#	echo "$goodplace"
#	#python3 cluePLACER.py $goodplace
#done

# this is the same as the commented-out loop above, reading through by line
while IFS= read -r -u13 line
do 
   python3 cluePLACER.py $line >> .wordplacementideal
done 13<".wordplacementideal"
