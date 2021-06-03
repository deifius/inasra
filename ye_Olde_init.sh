#!/usr/bin/env bash

#if [ "$#" -ne 1 ]; then
#    echo "You must enter exactly 1 command line arguments"
#    exit 1
#fi
mkdir -p users/$USER/$@
#cd users/$USER/$@
echo "$@"

test -f "acronym/links/$@" || ./WikiChomp.NU.py "$@"; clear
./Acronymizer.py "$@"
next_word_dir= users/$USER/$@
mkdir -p $next_word_dir/$next_word
python3 xword2jsonhtml.py xwordspine.json $next_word_dir > $next_word_dir/xword.json.html
#python3 xword2html.py xwordspine.json > users/$USER/$@/$next_word/xword.html
#echo $next_word
#./ye_Olde_init.sh $next_word
sleep 4
while $( ps -ef | grep cluePLACER | wc -l ) > 1
do
	sleep 3
    echo "...still too much clue placing going on"
done
sleep 2
while $( ps -aux|grep cluePLACER|wc|awk '{print $1}' ) > 1
do
	sleep 2
    echo "...not enough next move ideatin quite yet"
done
./whiptailCrystalizer.sh $next_word_dir/$next_word
