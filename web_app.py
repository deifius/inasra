#!/usr/bin/env python3

import os

os.system('./scripts/pips.sh -q > /dev/null')
os.system('./scripts/initdb.sh > /dev/null')

from flask import Flask, request, redirect, render_template, url_for
from subprocess import Popen, PIPE, STDOUT, check_output
import json, re, os, pwd, Acronymizer as acronymizer
import copy
from random import shuffle
import wikipedia, re
import wikichomp, spinylize
import inasra
import db

app = Flask(__name__)

global your_inasra

with open('emptyinasra.ipuz') as this:
	your_inasra = inasra.inasra(**json.loads(this.read()))

def web_acronymizer(word, relephants):
	acro_fren = acronymizer.acronymize(word, relephants)
	summary = db.get_word_summary(word)
	cont = db.get_word_content(word)
	content = re.split('\n+', re.sub('''['"]''', '', cont))
	for paragraph in content:
		if paragraph[0] == "=":
			content.remove(paragraph)
	this = render_template('word.html', word=word, summary=summary, wordupper=word[0].upper(), wordcapper=word.capitalize())
	for eachletter in enumerate(word): #Click Me!
		if eachletter[1] in [' ', '-', '.', ',','&'] or eachletter[0] == 0:
			this += ""
		elif eachletter[1] in ['{','(','[','}',')',']']:
			break
		else:
			ourletter = eachletter[1].capitalize()
			for paragraph in content:
				if acro_fren[eachletter[0]].lower() in paragraph.lower():
					paragraph = re.sub(acro_fren[eachletter[0]], f' {acro_fren[eachletter[0]].upper()}', paragraph, flags=re.IGNORECASE)
					insert_hover = f'title="{paragraph}"'
					#print(insert_hover)
					break
				else: insert_hover = f'title="no clue how {acro_fren[eachletter[0]]} relates to {word}"'
			this += f'''	<br>
							<a href='{acro_fren[eachletter[0]]}/{eachletter[0]}'{insert_hover}>
							<button type="button">
							<p style="font-family:monospace; line-height:.4"><font size='+2'>
							{ourletter} </font></p></button>&emsp;
							<div class="dropdown">
							<button class="dropbtn" style="height:35px;width:400px">
							{acro_fren[eachletter[0]]} &emsp;&emsp;&emsp;</button>
							<div class="dropdown-content">
					'''
			shuffle(relephants)
			for everyword in relephants:
				if everyword[0].lower() == eachletter[1].lower():
					for paragraph in content:
						if everyword.lower() in paragraph.lower():
							# TODO: Fix the bug with unbalanced parenthesis
							paragraph = re.sub(everyword, f' {everyword.upper()}', paragraph, flags=re.IGNORECASE)
							insert_hover = f'title="{paragraph}"'
							break
						else: insert_hover = f'title="no clue how {everyword} relates to {word}"'
					this += f"""<button><p style='line-height:.7'>
								<a href='{everyword}/{eachletter[0]}'{insert_hover}>
								{everyword}</a></p></button>"""
			this += f'''</div></div>'''
	return this

@app.route("/home")
@app.route("/")
def index():
	with open('emptyinasra.ipuz') as this:
		your_inasra = inasra.inasra(**json.loads(this.read()))
	#with open('.eggspine.txt','w') as egg: egg.write('')
	return render_template('home.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/<word>", methods=['POST'])
def recurs_spinalyze_post(word):
	return redirect("/"+word)

@app.route("/firstword/<word>")
@app.route("/<word>", methods=['GET'])
def recurs_spinalyze(word):
	try:
		wordspace_word = word#.replace(' ','')
		#if "(" in wordspace_word:
		#	wordspace_word = wordspace_word.split('(')[0]
		print(f'{word} is already in!') if word in ['favicon.ico'] + your_inasra.wordspace else your_inasra.wordspace.append(wordspace_word)
	except:
		print(f"couldn't add to the wordspace: {word}")
	relephants = db.get_word_links(word)
	if len(relephants) < 1:
		wikichomp.wikipedia_grab_chomp(word)
		relephants = db.get_word_links(word)
	print(f"{your_inasra.inasraid} {your_inasra.wordspace}, yo!")
	try:
		your_inasra.solution = spinylize.make_the_spine(your_inasra.wordspace[:-1]+[[your_inasra.wordspace[-1],0]])
		your_inasra.show_solution()
		#import pdb; pdb.set_trace()
		with open('currentspine.txt','w') as chacha: chacha.write(json.dumps(your_inasra.solution))
	except: print('no spine yet')
	return web_acronymizer(word, relephants)

@app.route('/first_word/', methods=['POST'])
def first_word():
	word = request.form['firstword']
	with open('emptyinasra.ipuz') as this:
		my_new_inasra = inasra.inasra(**json.loads(this.read()))
	# my_new_inasra.Start()
	print("starting word ", word)
	wikichomp.wikipedia_grab_chomp(word)
	print("did wikipedia_grab_chomp")
	my_new_inasra.title = word
	my_new_inasra.write_self_to_db()
	my_new_inasra.write_word_to_db(word)

	xword = request.form['firstword'].replace(' ','')
	for each_char in xword:
		my_new_inasra.add_one_row_Down()
	my_new_inasra.add_word_vert(xword, 0 , 0)
	my_new_inasra.wordspace.append(xword)
	# print(my_new_inasra.wordspace)
	# DEPRECATED
	os.system(f'mkdir -p users/$USER/{xword}')
	os.system(f'''echo '{my_new_inasra.dumps()}' > users/$USER/{xword}/{xword}.ipuz''')
	# DEPRECATED
	# your_inasra = my_new_inasra
	your_inasra = copy.deepcopy(my_new_inasra)
	# global your_inasra
	# your_inasra = copy.deepcopy(my_new_inasra)
	# print(f"we saved u a your_inasra: {your_inasra.inasraid}")
	# print(f"nevermind the bollocks here's the your_inasra: {your_inasra.dumps()}")
	return redirect("/"+word)

@app.route('/kenburns/<word>')
def kenburns(word):
	# lifted from https://codepen.io/anon/pen/XKWMaR
	all_image_urls = db.get_word_images(word)
	# these trashpictures really need to be excised before database insertion
	trashpictures = [
		'https://upload.wikimedia.org/wikipedia/commons/8/87/Gnome-mime-sound-openclipart.svg',
		'https://upload.wikimedia.org/wikipedia/en/9/94/Symbol_support_vote.svg',
		"https://upload.wikimedia.org/wikipedia/en/8/8a/OOjs_UI_icon_edit-ltr-progressive.svg",
		"https://upload.wikimedia.org/wikipedia/commons/f/fa/Wikiquote-logo.svg",
		"https://upload.wikimedia.org/wikipedia/en/4/4a/Commons-logo.svg",
		'https://upload.wikimedia.org/wikipedia/commons/f/ff/Wikidata-logo.svg',
		'https://upload.wikimedia.org/wikipedia/en/9/96/Symbol_category_class.svg',
		'https://upload.wikimedia.org/wikipedia/commons/f/fa/Wikibooks-logo.svg',
		'https://upload.wikimedia.org/wikipedia/commons/2/24/Wikinews-logo.svg',
		'https://upload.wikimedia.org/wikipedia/commons/f/fa/Wikiquote-logo.svg',
		'https://upload.wikimedia.org/wikipedia/commons/4/4c/Wikisource-logo.svg',
		'https://upload.wikimedia.org/wikipedia/commons/0/0b/Wikiversity_logo_2017.svg',
		'https://upload.wikimedia.org/wikipedia/en/4/4a/Commons-logo.svg',
		'https://upload.wikimedia.org/wikipedia/en/8/8a/OOjs_UI_icon_edit-ltr-progressive.svg',
		'https://upload.wikimedia.org/wikipedia/en/9/99/Question_book-new.svg',
		'https://upload.wikimedia.org/wikipedia/en/1/1b/Semi-protection-shackle.svg',
		'https://upload.wikimedia.org/wikipedia/en/d/db/Symbol_list_class.svg',
		'https://upload.wikimedia.org/wikipedia/en/0/06/Wiktionary-logo-v2.svg',
		'https://upload.wikimedia.org/wikipedia/commons/a/a4/Text_document_with_red_question_mark.svg',
		'https://upload.wikimedia.org/wikipedia/en/4/4a/Commons-logo.svg',
		'https://upload.wikimedia.org/wikipedia/en/8/8a/OOjs_UI_icon_edit-ltr-progressive.svg',
		'https://upload.wikimedia.org/wikipedia/en/f/f2/Edit-clear.svg'
	]
	for trash in trashpictures:
		try:
			all_image_urls.remove(trash)
		except: pass
	shuffle(all_image_urls)
	return render_template("kenburns.html", word=word, images=all_image_urls, imagequantity=len(all_image_urls))

@app.route('/framing/<word>')
def framing(word):
	return render_template('framingdevice.html', word=word)

@app.route("/<word>/<spine_pos>")
def build_the_spine(word, spine_pos):
	try: your_inasra.wordspace[-1] = [your_inasra.wordspace[-1], spine_pos]
	except: print(f"didn't add position to {your_inasra.wordspace}")
	spine_id = db.add_one_inasra_spine_please(your_inasra.inasraid, word, spine_pos)
	print(f"spine_pos: my word is {word}, my spine id is {spine_id}")
	return redirect(f'/{word}')

@app.route('/spine_peak')
def spine_look():
	try:
		return check_output(['./xword2html.py','currentspine.txt'])
	except: return 'no spine yet'

def crystalization(spine, wordbones):
	print(f'{json.dumps(spine)}\n{json.dums(wordbones)}')

if __name__ == "__main__":
	myuser_id = int(check_output(['id','-g']))
	app.run(debug=True, host="0.0.0.0", port=6000+myuser_id)
