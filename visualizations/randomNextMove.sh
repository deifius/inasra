#!/bin/bash

expressions=($(ls ../.NextMoves/*.png)) && echo "open ${expressions[$RANDOM % ${#expressions[@]} ]}"
