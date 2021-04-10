#!/usr/bin/env python3

from tabulate import tabulate
import json, re
from sys import argv

#Hallo I generate an html with buttons for letters to std
#input xwordspine.json
with open(argv[1]) as ok: spine = json.loads(ok.read())

jayzawn = {
  "title": "INASRA",
  "spine": spine,
  "#render": {
    "_": "<html hidden><meta charset=utf-8></html><script src=/render.js></script></html>",
    "css": "/styles.css"
  }
}

print(json.dumps(jayzawn, indent=2))
