# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Other
# Dav Project

# imports
import os
from sys import argv as args
import sys

sys.path.append(f'{os.environ["USERPROFILE"]}\\dav-cli')
import dav

def main():
	argv = list(map(str.lower, args[1:]))

	config = dav.get_config()

	if argv[0] in ['music']:
		path = config["modules"][argv[0]]["path"]
		complete_path = f"{os.environ['USERPROFILE']}\\{path}"
		os.chdir(complete_path)
		os.system("start .")

	elif argv[0] == 'edit':
		os.chdir("../../")
		os.system(f"{config['text_editor']} .")

	elif argv[0] == 'config':
		os.chdir("../../config")
		os.system(f"{config['text_editor']} config.json")

if __name__ == '__main__':
    main()