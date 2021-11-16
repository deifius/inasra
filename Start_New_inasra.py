#!/usr/bin/env python3

from whiptail import Whiptail
import json
from os import system
from lorem import text as lorem

def directory_initializer():
    for essentialdir in ['users','acronym/summary','acronym/content','acronym/links','acronym/images','.NextMoves' ]:
        system('mkdir -p ' + essentialdir)

def Color_Scheme():
    system("export NEWT_COLORS='\
    window=green,gray\
    border=black,green\
    textbox=green,black\
    button=black,green\
    title=green,black\
    root=lightgray,gray\
    entry=,black\
    roottext=green,gray\
    shadow=gray\
    actbutton=green,black\
    entry=green,black\
    '")
    print('color schemed!')

def WikiQueryPrep(word_or_phrase):
    ''' Hola pass me any string and I'll format it as a wikipedia article title.
        so "legislative chamber" becomes "Legislative_chamber"'''
    if ' ' in word_or_phrase:
        words = word_or_phrase.split(' ')
        wiki_article = words[0].capitalize() + "_" + '_'.join(words[1:])
        return wiki_article
    else: return word_or_phrase.capitalize()

def main():
    directory_initializer()
    Color_Scheme()
    new_adventure = Whiptail()
    new_adventure.title = "inasra welcomes you"
    new_adventure.backtitle = lorem()
    spinehead, exitstatus = new_adventure.inputbox('what shall you offer to inasra?')
    if exitstatus == 0:
        #this is where all the good sanitizing and CAP permutation should go
        system('./init_scrrrrp.sh ' + WikiQueryPrep(spinehead))

if __name__ == "__main__": main()
