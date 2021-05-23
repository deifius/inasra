#!/bin/bash

# Lifted from:
# https://unix.stackexchange.com/questions/155636/dialog-menu-to-display-files-and-select-one-of-them
[ -z "$1" ] && exit 1
[ -d $1 ] || exit 2

let i=0 # define counting variable
NextMoves=() # define working array
for line in $( ls .NextMoves ); do # process file by file
    let i=$i+1
    NextMoves+=("$i" "$line")
done

#for line in ${NextMoves[@]}; do; echo "$line"; done

FILE=$(whiptail --title "Here's your NextMoves" --menu "Chose one" 24 80 17 "${NextMoves[@]}" 3>&2 2>&1 1>&3) # show dialog and store output
echo lets do the whiptail
[ "$?" == 0 ] || exit 1

echo .NextMoves/"${NextMoves[$FILE * 2 - 1]}" $1${NextMoves[$FILE * 2 - 1]}
./decoherence.sh .NextMoves/"${NextMoves[$FILE * 2 - 1]}" $1${NextMoves[$FILE * 2 - 1]}

#clear
#if [ $? -eq 0 ]; then # Exit with OK
#    readlink -f $(ls -1 .NextMoves | sed -n "`echo "$FILE p" | sed 's/ //'`")
#fi
