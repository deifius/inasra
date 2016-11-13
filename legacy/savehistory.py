#!/usr/bin/env python3

import readline

def saveas(historyfile):
    savehandler = open(historyfile + ".history.py", 'w')
    for each_history in range(readline.get_current_history_length()):
        savehandler.write(str(readline.get_history_item(each_history)) + '\n')
    savehandler.close()
