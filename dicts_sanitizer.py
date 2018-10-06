#!/usr/bin/env python3

from glob import glob
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
		goodwords.append(pattern.sub('', every))

goodwords = set(goodwords)
numbers = re.compile('[0-9]')
badwords = []
for e in goodwords:
	if len(numbers.findall(e)) > 0:
		print(e)
		badwords.append(e)
for e in badwords:
	goodwords.remove(e)

goodwords = list(goodwords)
goodwords.sort()
##pdb.set_trace()

with open('OneBigDict.json','w') as writeitout:
	writeitout.write(json.dumps(goodwords))		


