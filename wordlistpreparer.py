#!/usr/bin/env python3

from glob import glob
import json
import re
from pdb import set_trace as st
from sys import argv

def get_acroglob():
	acroglob = []
	with open('.next_word_dir') as linkies:
		places_to_look = linkies.read().split('\n')
		for each_place in enumerate(places_to_look):
			if each_place[1] == "": places_to_look.pop(each_place[0])
			else: acroglob.append(each_place[1] + "links.json")
	return acroglob
def make_maybe_bone(acroglob):
	maybe_bone = []
	for each in acroglob:
		try: maybe_bone.append(json.loads(open(each).read().lower()))
		except FileNotFoundError as erer: print("none of this: " + each)
	return maybe_bone
def refine_goodwords(maybe_bone):
	with open("wiki_reserve_terms.json") as readio: reservewords =json.loads(readio.read())
	pattern = re.compile('[\W_]+')
	goodwords = []
	for each in maybe_bone:
		for every in each:
			if every.lower() not in reservewords:
				if re.search("[^a-zA-Z ]", every,) is None:
					#pdb.set_trace()
					goodwords.append(pattern.sub('', every).lower())
	return goodwords
def main():
	# freqygoodwords are sorted by frequency of recurrence of reference.
	# Most referred words are last, least are first
	goodwords = refine_goodwords(make_maybe_bone(get_acroglob()))
	freqygoodwords = sorted(set(goodwords), key = lambda ele: goodwords.count(ele))
	with open('freqygoodwords.json','w') as writeitout: writeitout.write(json.dumps(freqygoodwords))

if __name__ == '__main__': main()
