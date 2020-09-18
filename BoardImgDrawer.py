#!/usr/bin/env python3

from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from wand.compat import nested
from sys import argv
import subprocess
from pdb import set_trace
import json

FontSize = 12
with open(argv[1]) as readio: board =json.loads(readio.read())
#set_trace()
Width = len(board[0]) * FontSize
Height = len(board) * FontSize

with Drawing() as draw:
	with Image(width=Width, height=Height) as img:
		draw.font_family = 'Monospace'
		#draw.font_style = "Outline"
		draw.font_size = FontSize
		draw.push()
		#draw.text(0,80, 'Hello, world!')
		for row in enumerate(board):
			draw.text(int(Width/4),int(FontSize*(row[0]+2)),' '.join(row[1]))	
	
		#draw.text(0,40, 'waddup urf')
		draw.pop()
		draw(img)
		img.save(filename='image.png')

subprocess.call(['feh','image.png'])
