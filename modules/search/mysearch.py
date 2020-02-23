# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Search
# Dav Project

# imports 
from sys import argv
from sys import exit
import os
import subprocess
from difflib import SequenceMatcher
import sys

sys.path.append(f'{os.environ["USERPROFILE"]}\\dav-cli')
from dav import get_config

argv = list(map(str.lower, argv[1:]))

def main():
	config = get_config()

	print("use [exit] or [quit] to close")
	print("Search :")
	similarity = 0.8
	browser = config["modules"]["search"]["browser"]

	while 1:
		search = input("> ")
		if SequenceMatcher(a=search.lower(), b="exit").ratio() > similarity \
				or SequenceMatcher(a=search.lower(), b="quit").ratio() > similarity: exit(0)
		if len(search) > 0:
			if search.endswith(".com") or search.endswith(".pt") or search.endswith(".net"):
				subprocess.Popen(f"{browser} -incognito {search}", shell=True)
			else:
				subprocess.Popen(f"{browser} -new-tab -incognito \"? {search}\"", shell=True)
if __name__ == "__main__":
	main()