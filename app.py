#!/usr/env python3

from flask import Flask, request
import json
import os

app = Flask(__name__)


#Within app.py import the Flask module and create a web app using the following:


@app.route("/")
def index():
  with open('index.html') as ok: this=ok.read()
  return this;
#  return """
#  <h1>Python Flask in Docker!</h1>
#  <p>A sample web-app for running Flask inside Docker.</p>
#  """

@app.route('/wordgrid.json')
def wordgrid():
  with open('xwordspine.json') as ok: this=ok.read()
  return this

@app.route('/clueinsert', methods=["POST"])
def post():
	#return request.get_json(force=True)['insert']
	os.system('python3 clueinsert.py ' + request.get_json(force=True)['insert'])
	return "success"; # FIXME: check for actual success

#Finally, let's launch the app if the script is invoked as the main program:

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
