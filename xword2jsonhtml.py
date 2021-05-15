#!/usr/bin/env python3

import json, re
from sys import argv
from glob import glob

import pdb

import os

#Hallo I generate an html with buttons for letters to std
#input xwordspine.json
with open(argv[1]) as ok: spine = json.loads(ok.read())

jayzawn = {
  "title": "INASRA",
  "spine": spine,
  "metadata": {},
}

def recur(path):
  for f in glob(path+"/*"):
    if os.path.isdir(f):
      recur(f)
    elif re.match(".+json$", f):
      path_components = path.split("/")
      print("^"+("/".join(path_components[0:-2]))+"/([a-zA-Z_]+)/([a-zA-Z_]+).json$")
      m = re.match("^"+path+"/([a-zA-Z_]+)/([a-zA-Z_]+).json$", f)
      if m: jayzawn["metadata"][m.group(1)][m.group(2)] = json.loads(open(f).read())
    else:
      print("no match ya dummy: "+f)

recur(argv[2])

jayzawn["#render"] = {
  "_": "<html hidden><meta charset=utf-8></html><script src=/render.js></script></html>",
  "css": "/styles.css"
}

print(json.dumps(jayzawn, indent=2))
