#!/usr/bin/env bash


mkdir -p users/$USER/$@
#cd users/$USER/$@
#echo "$@"

test -f "acronym/links/$@" || ./WikiChomp.NU.py "$@"; clear
./Acronymizer.NU.py "$@" 
#mkdir -p users/$USER/$@/$next_word
#./ye_Olde_init.sh $next_word
