#!/usr/bin/env python3

from whiptail import Whiptail
import json
from os import system

def WikiQueryPrep(word_or_phrase):
    # Hola pass me any string and I'll format it as a wikipedia article title.
    # so "legislative chamber" becomes "Legislative_chamber"
    if ' ' in word_or_phrase:
        words = word_or_phrase.split(' ')
        wiki_article = words[0].capitalize() + "_" + '_'.join(words[1:])
        return wiki_article
    else: return word_or_phrase.capitalize()
    
def main():
    new_adventure = Whiptail()
    new_adventure.title = "inasra welcomes you"
    new_adventure.backtitle = "lots of stuff eventually"
    spinehead, exitstatus = new_adventure.inputbox('what will you offer to inasra?')
    if exitstatus == 0:
        #this is where all the good sanitizing and CAP permutation should go
        system('./init_scrrrrp.sh ' + WikiQueryPrep(spinehead))

if __name__ == "__main__": main()
