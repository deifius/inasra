#!/usr/bin/env python3

import pdb, re, json, sys
from boardtrim import boardtrim as trim
from time import sleep
from os import system

'''
	spinylize receives a code for an xword spine
	& makes that spine
	like a ribozome interpreting vertebrate DNA

'''
def visualize(xwordfield):
	#system('clear')
	#print('')
	for eachline in xwordfield:
		line = ' '
		linecheck = 0
		for each in eachline:
			line = line + ' ' + each
			if each != ' ':
				linecheck = 1

def get_the_egg():
	try:
		xwordspine,crystalizeds  = json.loads(sys.argv[1])
		#pdb.set_trace()
	except:
		with open('.eggspine.txt') as chicklet:
			xwordspine = chicklet.read().replace(' ','').split('\n')
		while xwordspine[-1] == '':
			xwordspine.pop()
		#pdb.set_trace()
		while xwordspine[-1][-1].isdigit() == False:
			xwordspine.pop()
		crystalizeds = []
		while xwordspine[-1][0].isalpha() == False:
			crystalizeds.append(xwordspine.pop())
		for each in enumerate(crystalizeds): crystalizeds[each[0]] = each[1].split('.')[1:]
		for each in enumerate(xwordspine):  xwordspine[each[0]] = each[1].split('\t')
	return [xwordspine, crystalizeds]

def make_the_spine(xwordspine):
	'''
	feed me a list of word,position(1d) pairs
	& I will return a 2d array of chars
	to serve as the spine for this inasra
	'''
	maxwordsize = {'verts':0,'horiz':0}
	if len(xwordspine)%2 == 0:
		verts = len(xwordspine[-1][0])+1
		horiz = len(xwordspine[-2][0])+1
	else:
		horiz = len(xwordspine[-1][0])+1
		verts = len(xwordspine[-2][0])+1 if len(xwordspine) >= 2 else 0

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
				#visualize(xwordfield)
				#sleep(.011)
			if cursor[0] > maxcursor[0]:
					maxcursor[0] = cursor[0]
			cursor[0] -= len(xwordspine[eachword][0])
			cursor[0] += int(xwordspine[eachword][1])
		if eachword%2 != 0:
			for letter in xwordspine[eachword][0]:
				xwordfield[cursor[0]][cursor[1]] = letter
				cursor[1] += 1
				#visualize(xwordfield)
				#sleep(.011)
			if cursor[1] > maxcursor[1]:
					maxcursor[1] = cursor[1]
			cursor[1] -= len(xwordspine[eachword][0])
			cursor[1] += int(xwordspine[eachword][1])
			#pdb.set_trace()
	return trim(list(zip(*trim(xwordfield))))

def write_it_down(xwordfield):
	with open('xwordspine.json', 'w') as writio:
		writio.write(json.dumps(xwordfield))

def main():
	xwordspine, crystalizeds =  get_the_egg()
	xwordfield = make_the_spine(xwordspine)
	#for e in xwordfield: print(' '.join(e))
	#for e in crystalizeds: print(e)
	write_it_down(xwordfield)
	return xwordfield

if __name__ == '__main__': main()
