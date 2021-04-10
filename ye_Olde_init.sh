#!/usr/bin/env bash

#if [ "$#" -ne 1 ]; then
#    echo "You must enter exactly 1 command line arguments"
#    exit 1
#fi
mkdir -p users/$USER/$@
#cd users/$USER/$@
echo "$@"

test -f "acronym/links/$@" || ./WikiChomp.NU.py "$@"; clear
./Acronymizer.NU.py "$@"
next_word_dir = users/$USER/$@/$next_word
mkdir -p $next_word_dir
#python3 xword2html.py xwordspine.json > users/$USER/$@/$next_word/xword.html
python3 xword2jsonhtml.py xwordspine.json $next_word_dir > $next_word_dir/xword.json.html
#echo $next_word
#./ye_Olde_init.sh $next_word
