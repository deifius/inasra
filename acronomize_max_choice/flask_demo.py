#!/usr/bin/env python3

from flask import Flask, request, redirect
from subprocess import Popen, PIPE, STDOUT
import json, re, os, acronymizer
from random import shuffle
import wikipedia
import wikichomp

app = Flask(__name__)

def the_singular_thing(word, relephants):
	acro_fren = acronymizer.acronymize(word, relephants)
	with open('index.html') as stuff: this = stuff.read()
	with open('../acronym/summary/'+word) as summ: summary = json.loads(summ.read())
	this += f'''
	<a href=" " title="{summary}" style="background-color:#FFFFFF;color:#000000;text-decoration:none"><h1>{word}</h1></a>
	'''
	for eachletter in enumerate(word):#Click Me!
		if eachletter[1] == ' ':
			this += "<br>"
		else:
			this += f'''
			<br>
			<a href='{acro_fren[eachletter[0]]}'><button type="button"><h2>{eachletter[1]}</h2></button>&emsp;
			<div class="dropdown">
			<button class="dropbtn">{acro_fren[eachletter[0]]}</button>
			<div class="dropdown-content">\n'''
			shuffle(relephants)
			for everyword in relephants:
				if everyword[0].lower() == eachletter[1].lower():
					this += f"<a href='{everyword}'><button>{everyword}</button></a>"
			this += '''</div></div>'''
	this +='''</body></html>'''
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
    <input type="submit" value="beginasration">
  </div>
</form>
'''
	return this

@app.route("/firstword/<word>")
@app.route("/<word>")
def recurs_spinalyze(word):
	try:
		with open('../acronym/links/'+word) as linkies:
			relephants = json.loads(linkies.read())
		#return json.dumps(relephants)
	except FileNotFoundError:
		wikichomp.wikipedia_grab_chomp(word)
		with open('../acronym/links/'+word) as linkies:
			relephants = json.loads(linkies.read())
	return the_singular_thing(word, relephants)

@app.route('/first_word/', methods=['POST'])
def first_word():
	word = "/"+request.form['firstword']
	return redirect(word)
	#recurs_spinalyze(firstword)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
