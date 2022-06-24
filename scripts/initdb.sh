#!/bin/bash
if [ -f "inasra.sqlite3" ]
then
  echo "The file inasra.sqlite3 already exists. Please remove it first if you want to create a new database."
  exit 1
fi

sqlite3 inasra.sqlite3 < inasra.sql
