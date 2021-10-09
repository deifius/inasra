#!/usr/bin/env python3

import json
from sys import argv


def main():
    Forget = argv[1].split('/')[-1].split('.')[0]
    print(Forget)
    with open('freqygoodwords.json') as freqy: freqs = json.loads(freqy.read())
    freqs.remove(Forget)
    with open('freqygoodwords.json','w') as freqy: freqy.write(json.dumps(freqs))

if __name__ == "__main__":  main()
