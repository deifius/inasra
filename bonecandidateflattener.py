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

pdb.set_trace()

flat_list_of_maybe_bones = []
for each in maybe_bone:
	for every in each:
 		for single in every:
 			flat_list_of_maybe_bones.append(single)


flat_list_of_maybe_bones[random.randint(0,len(flat_list_of_maybe_bones))]
