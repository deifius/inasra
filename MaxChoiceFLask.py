#!/usr/bin/env python3

from flask import Flask, request, redirect, render_template, url_for
from subprocess import Popen, PIPE, STDOUT, check_output
import json, re, os, pwd, Acronymizer as acronymizer
from random import shuffle
import wikipedia, re
import wikichomp
import inasra

app = Flask(__name__)

def the_singular_thing(word, relephants):
	acro_fren = acronymizer.acronymize(word, relephants)
	with open('acronym/summary/'+word) as summ: summary = json.loads(summ.read()).split('\n')[0]
	with open('acronym/content/'+word) as cont:
		content = re.split('\n+',re.sub('''['"]''','',json.loads(cont.read())))
		for paragraph in content:
			if paragraph[0] == "=":
				content.remove(paragraph)
	this = render_template('word.html', word= word, summary=summary,wordupper=word[0].upper(), wordcapper=word.capitalize())
	for eachletter in enumerate(word):#Click Me!
		if eachletter[1] in [' ', '-', '.', ',','&'] or eachletter[0] == 0:
			this += ""
		else:
			ourletter = eachletter[1].capitalize()
			for paragraph in content:
				if acro_fren[eachletter[0]].lower() in paragraph.lower():
					paragraph = re.sub(acro_fren[eachletter[0]], f' {acro_fren[eachletter[0]].upper()}', paragraph, flags=re.IGNORECASE)
					insert_hover = f'title="{paragraph}"'
					print(insert_hover)
					break
				else: insert_hover = f'title="no clue how {acro_fren[eachletter[0]]} relates to {word}"'
			this += f'''
			<br>
			<a href='{acro_fren[eachletter[0]]}'{insert_hover}><button type="button"><p style="font-family:monospace; line-height:.4"><font size='+2'> {ourletter} </font></p></button>&emsp;
			<div class="dropdown">
			<button class="dropbtn" style="height:35px;width:400px"> {acro_fren[eachletter[0]]} &emsp;&emsp;&emsp;</button>
			<div class="dropdown-content">'''
			shuffle(relephants)
			for everyword in relephants:
				if everyword[0].lower() == eachletter[1].lower():
					for paragraph in content:
						if everyword.lower() in paragraph.lower():
							paragraph = re.sub(everyword, f' {everyword.upper()}', paragraph, flags=re.IGNORECASE)
							insert_hover = f'title="{paragraph}"'
							break
						else: insert_hover = f'title="no clue how {everyword} relates to {word}"'
					this += f"<button><p style='line-height:.7'><a href='{everyword}'{insert_hover}>{everyword}</a></p></button>"
			this += f'''</div></div>'''
	return this

@app.route("/home")
@app.route("/")
def index():
	return render_template('home.html')

@app.route("/about")
def about():
	return render_template('about.html')


@app.route("/firstword/<word>")
#@app.route("/<otherwords>/<word>")
@app.route("/<word>")
def recurs_spinalyze(word):
	try:
		with open('acronym/links/'+word) as lizninks:
			relephants = json.loads(lizninks.read())
	except FileNotFoundError:
		wikichomp.wikipedia_grab_chomp(word)
		with open('acronym/links/'+word) as lizninks:
			relephants = json.loads(lizninks.read())
	return the_singular_thing(word, relephants)

@app.route('/first_word/', methods=['POST'])
def first_word():
	word = "/"+request.form['firstword']
	with open('emptyinasra.ipuz') as this:
		my_new_inasra = inasra.inasra(**json.loads(this.read()))
	xword = request.form['firstword'].replace(' ','')
	for each_char in xword:
		my_new_inasra.add_one_row_Down()
	my_new_inasra.add_word_vert(xword, 0 , 0)
	os.system(f'mkdir -p users/$USER/{xword}')
	os.system(f'''echo '{my_new_inasra.dumps()}' > users/$USER/{xword}/{xword}.ipuz''')
	return redirect(word)

@app.route('/kenburns/<word>')
def kenburns(word):
	# lifted from https://codepen.io/anon/pen/XKWMaR
	with open(f'acronym/images/{word}') as kenny: all_image_urls = json.loads(kenny.read())
	# these trashpictures really need to be excised before database insertion
	trashpictures = ['https://upload.wikimedia.org/wikipedia/commons/8/87/Gnome-mime-sound-openclipart.svg',
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
	'https://upload.wikimedia.org/wikipedia/en/0/06/Wiktionary-logo-v2.svg'
]
	for trash in trashpictures:
		try:
			all_image_urls.remove(trash)
		except:
			print(f'{trash} not found')
	shuffle(all_image_urls)
	return render_template("kenburns.html", word=word, images=all_image_urls, imagequantity=len(all_image_urls))

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)
