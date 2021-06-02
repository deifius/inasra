#!/usr/bin/env python3

from whiptail import Whiptail
import json
from os import system
def main():
    new_adventure = Whiptail()
    new_adventure.title = "inasra welcomes you"
    new_adventure.backtitle = "lots of stuff eventually"
    spinehead = new_adventure.inputbox('what will you offer to inasra?')
    #this is where all the good sanitizing and CAP permutation should go
    system('./init_scrrrrp.sh ' + spinehead[0])
if __name__ == "__main__": main()
