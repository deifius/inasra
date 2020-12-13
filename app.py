#!/usr/bin/env python3

from flask import Flask, request
from glob import glob
import json
import os

app = Flask(__name__)


#Within app.py import the Flask module and create a web app using the following:



@app.route("/")
def index():
  with open("public/index.html") as ok: this=ok.read()
  return this;
#  return """
#  <h1>Python Flask in Docker!</h1>
#  <p>A sample web-app for running Flask inside Docker.</p>
#  """

@app.route("/index.js")
def js():
  with open("public/index.js") as ok: this=ok.read()
  return this;

@app.route("/styles.css")
def css():
  with open("public/styles.css") as ok: this=ok.read()
  return this;

@app.route("/ipuz.json")
def ipuz():
  with open("example.ipuz") as ok: this=ok.read()
  return this

@app.route("/wordgrid.json")
def wordgrid():
  with open("xwordspine.json") as ok: this=ok.read()
  return this

@app.route("/nextmoves.json")
def nextmoves():
  nextmovesglob = glob(".NextMoves/*")
  nextmovesdict = {}
  for nextmove in nextmovesglob:
    with open(nextmove) as ok: nextmovesdict[nextmove]=json.loads(ok.read())
  return nextmovesdict

@app.route("/clueinsert", methods=["POST"])
def post():
	#return request.get_json(force=True)["insert"]
	os.system("python3 clueinsert.py " + request.get_json(force=True)["insert"])
	return "success"; # FIXME: check for actual success

#Finally, let"s launch the app if the script is invoked as the main program:

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
