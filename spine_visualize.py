#!/usr/bin/env python
import pdb
import json

# TODO : populate the field with the words

xwordspine = open('inasrafieldtest.txt').read().replace(' ','').split('\n')
if xwordspine[-1] == '':
	xwordspine.pop(-1)
for each in range(len(xwordspine)):
	xwordspine[each] = xwordspine[each].split('\t')
if len(xwordspine)%2 == 0:
	verts = len(xwordspine[-1][0])+1
	horiz = len(xwordspine[-2][0])+1
else:
	horiz = len(xwordspine[-1][0])+1
	verts = len(xwordspine[-2][0])+1

for eachword in range(len(xwordspine)):
	if eachword%2 == 0:
		verts += int(xwordspine[eachword][1])
	if eachword%2 != 0:
		##pdb.set_trace()
		horiz += int(xwordspine[eachword][1])
#approximate size of grid sized to contain a spine  
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
			#pdb.set_trace()
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
print('')
for eachline in xwordfield:
	line = ' '
	for each in eachline:
		line = line + ' ' + each
	print(line)

writio = open('xwordspine.json', 'w')
writio.write(json.dumps(xwordfield))
writio.close()
#pdb.set_trace()
#print("verts:", verts)
#print('horiz', horiz)
