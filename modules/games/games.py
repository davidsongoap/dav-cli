# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Games
# Dav Project

# imports
import dav
from sys import argv
from sys import exit
import subprocess
import sys
import os

from difflib import SequenceMatcher
sys.path.append(f'\"{os.environ["USERPROFILE"]}\\dav-cli\"')

config = dav.get_config()


def main():
	args = list(map(str.lower, argv[1:]))
	similarity = 0.8

	if len(args) == 0:
		print("no game selected!")
		print("use dav games <gametitle>")
		print("or dav games [list] for the games available")
		exit(0)

	game = args[0].lower()

	if SequenceMatcher(a=game, b="tron").ratio() > similarity:
		subprocess.Popen(f"{config['browser']} https://davidsongoap.github.io/tronjs/", shell=True)

	elif SequenceMatcher(a=game, b="list").ratio() > similarity:
		print("""Game List:
	tron""")
		exit(0)
	else:
		print("""
Invalid game 
use games [list] for the games available""")


if __name__ == '__main__':
	main()
