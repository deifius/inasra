#!/usr/bin/env python3

from glob import glob as glob
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
		goodwords.append(pattern.sub('', every))

writeitout = open('OneBigDict.json','w')
writeitout.write(json.dumps(goodwords))		
writeitout.close()

