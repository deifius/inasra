#!/usr/bin/env python3

from glob import glob
import json
import re
import pdb

acroglob = glob('acronym/links/*')
maybe_bone = []
for each in acroglob:
	maybe_bone.append(json.loads(open(each).read().lower()))

with open("wiki_reserve_terms.json") as readio: reservewords =json.loads(readio.read())

pattern = re.compile('[\W_]+')
goodwords = []
for each in maybe_bone:
	for every in each:
		if every.lower() not in reservewords:
			if re.search("[^a-zA-Z ]", every,) is None:
				#pdb.set_trace()
				goodwords.append(pattern.sub('', every).lower())

freqygoodwords = sorted(set(goodwords), key = lambda ele: goodwords.count(ele))
# freqygoodwords are sorted by frequency of recurrence of reference.
# Most referred words are last, least are first
#pdb.set_trace()

with open('freqygoodwords.json','w') as writeitout: writeitout.write(json.dumps(freqygoodwords))
