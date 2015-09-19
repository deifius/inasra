#!/usr/bin/env python
import pdb
# TODO 

xwordspine = open('inasrafieldtest.txt').read().split('\n')
if xwordspine[-1] == '':
	xwordspine.pop(-1)
for each in range(len(xwordspine)):
	xwordspine[each] = xwordspine[each].split('\t')
verts = 0
horiz = 0
for eachword in range(len(xwordspine)):
	if eachword%2 == 0:
		for eachletter in xwordspine[eachword][0]:
			verts += 1
		horiz -= int(xwordspine[eachword][1])
	if eachword%2 != 0:
		#pdb.set_trace()
		for eachletter in xwordspine[eachword][0]:
			horiz += 1
		verts -= int(xwordspine[eachword][1])
xwordfield = []
for everyletter in range(verts):
	xwordfield.append([])
for everyletter in range(horiz):
	for everyvert in range(verts):
		xwordfield[everyvert].append(' ')

for eachword in range(len(xwordspine)):
	

for eachline in xwordfield:	print(eachline)
print("verts:", verts)
print('horiz', horiz)
