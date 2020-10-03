#!/usr/bin/env python3

from glob import glob
import random
import json
import re
import pdb

acroglob = glob('acro_dicts/*')
maybe_bone = []
for each in acroglob:
	maybe_bone.append(json.loads(open(each).read()))

reservewords = json.loads(open('wiki_reserve_terms.json').read())
pattern = re.compile('[\W_]+')
goodwords = []
for each in maybe_bone:
	for every in each:
		if every in reservewords: continue
		goodwords.append(pattern.sub('', every[0]))
		#pdb.set_trace()

flat_list_of_maybe_bones = []
for each in maybe_bone:
	for every in each:
		for single in every:
			flat_list_of_maybe_bones.append(single)


flat_list_of_maybe_bones[random.randint(0,len(flat_list_of_maybe_bones))]
