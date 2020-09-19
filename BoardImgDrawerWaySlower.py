#!/usr/bin/env python3

from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from wand.compat import nested
from sys import argv
import subprocess
from pdb import set_trace
import json

FontSize = 22
with open(argv[1]) as readio: board =json.loads(readio.read())
#set_trace()
Width = int((len(board[0])+2) * FontSize * .8)
Height = int((len(board)+2) * FontSize )
FileName=argv[1]+'.png'

with Drawing() as draw:
	with Image(width=Width, height=Height) as img:
		draw.font_family = "Times New Roman"
		#draw.font_style = "Outline"
		draw.font_size = FontSize
		draw.push()
		for row in enumerate(board):
			for letter in enumerate(row[1]):
				draw.text(int(.8*FontSize*(letter[0]+1)),int(.8*FontSize*(row[0]+9)),letter[1])	
		draw.pop()
		draw(img)
		img.save(filename=FileName)

subprocess.call(['feh',FileName])
