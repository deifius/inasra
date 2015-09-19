#!/usr/bin/env python
import pdb
# TODO : populate the field with the words

xwordspine = open('inasrafieldtest.txt').read().split('\n')
if xwordspine[-1] == '':
	xwordspine.pop(-1)
for each in range(len(xwordspine)):
	xwordspine[each] = xwordspine[each].split('\t')
if len(xwordspine)%2 == 0:
	verts = len(xwordspine[-1][0])
	horiz = len(xwordspine[-2][0])
else:
	horiz = len(xwordspine[-1][0])
	verts = len(xwordspine[-2][0])

for eachword in range(len(xwordspine)):
	if eachword%2 == 0:
		verts += int(xwordspine[eachword][1])
	if eachword%2 != 0:
		##pdb.set_trace()
		horiz += int(xwordspine[eachword][1])
xwordfield = []
for everyletter in range(verts):
	xwordfield.append([])
for everyletter in range(horiz):
	for everyvert in range(verts):
		xwordfield[everyvert].append(' ')
cursor = [0,0]
for eachword in range(len(xwordspine)):
	if eachword%2 == 0:
		for letter in xwordspine[eachword][0]:
			xwordfield[cursor[0]][cursor[1]] = letter
			cursor[0] += 1
		cursor[0] -= len(xwordspine[eachword][0])
		cursor[0] += int(xwordspine[eachword][1])
		#pdb.set_trace()
	if eachword%2 != 0:
		for letter in xwordspine[eachword][0]:
			xwordfield[cursor[0]][cursor[1]] = letter
			cursor[1] += 1
		cursor[1] -= len(xwordspine[eachword][0])
		cursor[1] += int(xwordspine[eachword][1])
		#pdb.set_trace()
for eachline in xwordfield:	print(eachline)

print("verts:", verts)
print('horiz', horiz)
