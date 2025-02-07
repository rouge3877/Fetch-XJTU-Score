#!/usr/bin/env zsh

mkdir -p score_pages

python3 src/main.py -s cookies.txt $1  | python3 src/generate_html.py $1 -s > score_pages/$1.html
google-chrome score_pages/$1.html
