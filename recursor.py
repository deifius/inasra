#!/usr/bin/env python

import json
import sys
import pdb
import random

# this is the recursor of inasra.  it creates depth in the inasra array.  \
# TODO arbitrary ndimension inasra spider
# implemented in python3

inasra = []

def self_recursion(inasra):
	if len(sys.argv) != 2:
		ux = input("what is your inasra?\t")
	else:
		ux = sys.argv[1]
	while 1:		    
		inasra = json.loads(open("acro_dicts/" + ux).read())
		#pdb.set_trace()
		if ux == '':	continue
		if inasra == []:
			for each in range(len(ux)):
				inasra.append([ux[each]])
		elif isinstance(ux, str):
			#pdb.set_trace()
			for each in range(len(inasra)):
				if inasra[each][0] == ux[0]:
					inasra[each].append(ux)
# this resets the array with a seed of user choice
		if ux.isdigit():
			print('choose one:')
			if int(ux) < len(inasra) and int(ux) > -1:
				oldux = ux
				ux = input(inasra[int(ux)])
				ux = inasra[int(oldux)][int(ux)]
			inasra = []
			for each in range(len(ux)):
				inasra.append([ux[each]])
			print('\n')
		print(ux + " acronymized:")
		running_acronym = []
		selection = 0
		# now generate a random acronym from the dictionary
		# && recursify
		for each in inasra:
			if each in ['','.']:
				print(each)
			else:
				running_acronym.append(random.choice(each))
				print(str(selection) + ".\t" + running_acronym[-1][0].title() + " \t" + running_acronym[-1].capitalize())
				selection+= 1
		userchoice = -1
		print("\n" + ux + " acronymized!")
		#pdb.set_trace()
		ux = running_acronym[int(input('what is your inasra?\t'))]
self_recursion(inasra)

#In current state it is a forgetting, n-dimension inasra
