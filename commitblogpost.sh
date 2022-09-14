#!/bin/zsh
# script to auto-commit a folder to github pages.

# Get to correct git folder
cd '/Users/albertsikkema/Documents/Dev - Prive/albertsikkema.github.io/'

git add .

git commit -m "auto commit" $1

git push origin main


