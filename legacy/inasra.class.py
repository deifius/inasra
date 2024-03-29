import pdb
import json
from time import sleep
from os import system
import re
import ipuz



def visualize(xwordfield):
	system('clear')
	print('')
	for eachline in xwordfield:
		line = ' '
		linecheck = 0
		for each in eachline:
			line = line + ' ' + each
			if each != ' ':
				linecheck = 1
		if linecheck == 1:
			print(line)

maxwordsize = {'verts':0,'horiz':0}
xwordspine = open('.eggspine.txt').read().replace(' ','').split('\n')
if xwordspine[-1] == '':
	xwordspine.pop(-1)
#pdb.set_trace()
if xwordspine[-1][-1].isdigit() == False:
	xwordspine.pop(-1)
for each in range(len(xwordspine)):
	xwordspine[each] = xwordspine[each].split('\t')
if len(xwordspine)%2 == 0:
	verts = len(xwordspine[-1][0])+1
	horiz = len(xwordspine[-2][0])+1
else:
	horiz = len(xwordspine[-1][0])+1
	verts = len(xwordspine[-2][0])+1

pattern = re.compile('[\W_]+')
for each in xwordspine:
	each[0] = pattern.sub('', each[0])
#pdb.set_trace()

for eachword in range(len(xwordspine)):
	if eachword%2 == 0:
		verts += int(xwordspine[eachword][1])
		if len(xwordspine[eachword][0])>maxwordsize['verts']:
			maxwordsize['verts']= len(xwordspine[eachword][0])
	if eachword%2 != 0:
		##pdb.set_trace()
		horiz += int(xwordspine[eachword][1])
		if len(xwordspine[eachword][0])>maxwordsize['horiz']:
			maxwordsize['horiz']= len(xwordspine[eachword][0])
#approximate size of grid sized to contain a spine
#TODO: needs to be exact, not approximate
xwordfield = []
verts += maxwordsize['verts']
horiz += maxwordsize['horiz']
for everyletter in range(verts):
	xwordfield.append([])
for everyletter in range(horiz):
	for everyvert in range(verts):
		xwordfield[everyvert].append(' ')
cursor = [0,0]
maxcursor = cursor
for eachword in range(len(xwordspine)):
	if eachword%2 == 0:
		for letter in xwordspine[eachword][0]:
			xwordfield[cursor[0]][cursor[1]] = letter
			cursor[0] += 1
			visualize(xwordfield)
			sleep(.031)
		if cursor[0] > maxcursor[0]:
				maxcursor[0] = cursor[0]
		cursor[0] -= len(xwordspine[eachword][0])
		cursor[0] += int(xwordspine[eachword][1])
	if eachword%2 != 0:
		for letter in xwordspine[eachword][0]:
			xwordfield[cursor[0]][cursor[1]] = letter
			cursor[1] += 1
			visualize(xwordfield)
			sleep(.031)
		if cursor[1] > maxcursor[1]:
				maxcursor[1] = cursor[1]
		cursor[1] -= len(xwordspine[eachword][0])
		cursor[1] += int(xwordspine[eachword][1])
		#pdb.set_trace()



with open('xwordspine.json', 'w') as writio:
	writio.write(json.dumps(xwordfield))

# TODO : populate the spine with the words from acro_dicts. This is project crystalyzation.py
