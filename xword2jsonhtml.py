#!/usr/bin/env python3

import json, re
from sys import argv
from glob import glob

import os

#Hallo I generate an html with buttons for letters to std
#input xwordspine.json
with open(argv[1]) as ok: spine = json.loads(ok.read())

jayzawn = {
  "title": "INASRA",
  "spine": spine,
}

for f in glob(argv[2]+"/*.json"):
  jayzawn[re.match("^"+argv[2]+"/(.+).json$", f).group(1)] = json.loads(open(f).read())

jayzawn["#render"] = {
  "_": "<html hidden><meta charset=utf-8></html><script src=/render.js></script></html>",
  "css": "/styles.css"
}

print(json.dumps(jayzawn, indent=2))
