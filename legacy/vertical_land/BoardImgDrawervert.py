#!/usr/bin/env python3

from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from wand.compat import nested
from sys import argv
import subprocess
from pdb import set_trace
import json

FontSize = 16
#if argv[2]:
#	board = json.loads(argv[2])
#else:
with open(argv[1]) as readio: board =json.loads(readio.read())
#set_trace()

# The width & height formulas were deleloped w/ guess & check
# Anyone who knows enough about fonts to build more precise algorithms?
Width = int((len(board[0])+1) * FontSize * .65)
Height = int((len(board)+2) * FontSize * .7)
FileName=argv[1]+'.png'

with Drawing() as draw:
	with Image(width=Width, height=Height) as img:
		draw.font_family = 'Fixed'
		# the font need not only be monotype, but spaces must have the same weight as characters
		draw.font_style = "normal"
		draw.stroke_color = Color('Red')
		draw.font_size = FontSize
		draw.push()
		for row in enumerate(board):
			#for letter in enumerate(row[1]):
			#	set_trace()
			#	if letter[1] == " ":
			#		board[row[0]][letter[0]] = " "
			#set_trace()
			draw.text(int(FontSize),int(.7*FontSize*(row[0]+2)),''.join(row[1]))
			# Font placement here is dependant on more guess&check spacing issues
		draw.pop()
		draw(img)
		img.save(filename=FileName)

#subprocess.call(['feh',FileName])
