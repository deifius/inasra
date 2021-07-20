#!/usr/bin/env bash

#if [ "$#" -ne 1 ]; then
#    echo "You must enter exactly 1 command line arguments"
#    exit 1
#fi
mkdir -p users/$USER/$@
test -f "acronym/links/$@" || ./WikiChomp.NU.py "$@"; clear
./Acronymizer.py "$@"
next_word_dir=users/$USER/$@
mkdir -p $next_word_dir/$next_word
python3 xword2jsonhtml.py xwordspine.json $next_word_dir > $next_word_dir/xword.json.html
echo "$next_word_dir/$next_word" >> .next_word_dir
export inasradir=$next_word_dir
echo inasradir=$inasradir
