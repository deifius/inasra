#!/usr/bin/env python3

from flask import Flask, request, redirect
from subprocess import Popen, PIPE, STDOUT, check_output
import json, re, os, pwd, Acronymizer as acronymizer
from random import shuffle
import wikipedia, re
import wikichomp
import inasra

app = Flask(__name__)

def the_singular_thing(word, relephants):
	acro_fren = acronymizer.acronymize(word, relephants)
	with open('index.html') as stuff: this = stuff.read()
	with open('acronym/summary/'+word) as summ: summary = json.loads(summ.read())
	with open('acronym/content/'+word) as cont:
		content = re.split('\n+',re.sub('''['"]''','',json.loads(cont.read())))
		for paragraph in content:
			if paragraph[0] == "=":
				content.remove(paragraph)
	this += f'''
	<a href= ''{summary}><button type="button"><p style="font-family:monospace;"><h1> {word[0]} </p></button>&emsp;
	<a href=" " title="{summary}" style="background-color:#FFFFFF;color:#000000;text-decoration:none">{word}</h1></a>
	'''
	for eachletter in enumerate(word):#Click Me!
		if eachletter[1] == ' ' or eachletter[0] == 0:
			this += "<br>"
		else:
			ourletter = eachletter[1].capitalize()
			for paragraph in content:
				if acro_fren[eachletter[0]].lower() in paragraph.lower():
					insert_hover = f'title="{paragraph}"'
					print(insert_hover)
					break
				else: insert_hover = f'title="no clue how {acro_fren[eachletter[0]]} relates to {word}"'
			this += f'''
			<br>
			<a href='{acro_fren[eachletter[0]]}'{insert_hover}><button type="button"><p style="font-family:monospace;"><h2> {ourletter} </h2></p></button>&emsp;
			<div class="dropdown">
			<button class="dropbtn"> {acro_fren[eachletter[0]]} </button>
			<div class="dropdown-content">\n'''
			shuffle(relephants)
			for everyword in relephants:
				if everyword[0].lower() == eachletter[1].lower():
					this += f"<a href='{everyword}'><button>{everyword}</button></a>"
			this += '''</div></div>'''
	this +=f'''</body></html>'''
	return this

@app.route("/")
def index():
	this = f'''
<form action="/first_word/" method="post">
  <div>
    <label for="example">This is where the inasra happens<br></label>
	<input type="text" id="example" size="40" placeholder="What do you offer to inasra" name="firstword">
  </div>
  <div>
    <input type="submit" value="beginasrazion">
  </div>
</form>
'''
	return this

@app.route("/firstword/<word>")
#@app.route("/<otherwords>/<word>")
@app.route("/<word>")
def recurs_spinalyze(word):
	try:
		with open('acronym/links/'+word) as linkies:
			relephants = json.loads(linkies.read())
		#return json.dumps(relephants)
	except FileNotFoundError:
		wikichomp.wikipedia_grab_chomp(word)
		with open('acronym/links/'+word) as linkies:
			relephants = json.loads(linkies.read())
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
	#inasra_path = f'users/{pwd.getpwuid( os.getuid() )[ 0 ]}'
	#inasra_path += word
	#return inasra_path
	return redirect(word)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)
