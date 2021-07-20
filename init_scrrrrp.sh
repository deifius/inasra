#!/bin/bash

rm .NextMoves/* 2> /dev/null
rm acro_dicts/* 2> /dev/null
rm acronym/*/* #a bunch of stuff
rm .next_word_dir
rm .eggspine.txt
touch .eggspine.txt

ps -ef|grep visualise | grep -v grep || xfce4-terminal -e  './visualizations/bashvisualise.py'
./ye_Olde_init.sh $1
#python3 wikichomp_py3.py
python3 spinylize.py
python3 boardtrim.py
python3 wordlistpreparer.py
echo "words sanitized"
python3 nextbestwords.py &
bestwords=$!
#python3 vertical_land/VERTnextbestwords.py &
vertwords=$!

sleep 2
while [ $(ps -ef | grep cluePLACER | wc -l) -gt 1 ]
do
	sleep 3
    echo "...still too much clue placing going on"
done
while [ ! -f .next_word_dir ]; do
	sleep 2;
	echo "waiting on the secret next_word_dir"
done
./whiptailCrystalizer.sh $(head -n 1 .next_word_dir)
