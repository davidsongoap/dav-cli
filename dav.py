# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Dav
# Dav Project

import sys
from sys import exit
from sys import argv as args
from difflib import SequenceMatcher
import os
import json

if sys.version_info[0] < 3:
	print("Dav is only compatible with Python 3 :(")
	exit(0)


# read file
def get_config():
	with open(f'{os.environ["USERPROFILE"]}\\dav-cli\\config\\config.json', 'r') as myfile:
		read_data = myfile.read()
	myfile.close()
	return json.loads(read_data)


def main():
	argv = args[1:]

	if (len(argv) == 0):
		print("""
██████╗  █████╗ ██╗   ██╗
██╔══██╗██╔══██╗██║   ██║
██║  ██║███████║██║   ██║
██║  ██║██╔══██║╚██╗ ██╔╝
██████╔╝██║  ██║ ╚████╔╝
╚═════╝ ╚═╝  ╚═╝  ╚═══╝

Welcome to Dav
use dav [module] <args>
use dav [help] or [h] for help""")
		exit(0)

	argv = list(map(str.lower, argv))
	arg_mod = argv[0]
	ar = " ".join(argv[1:])

	module_list = []
	config = get_config()

	modules = config["modules"]
	tags = []

	similarity = 0.8
	for mod_name in list(modules.keys()):
		module_list.append(mod_name)
		mod = modules[mod_name]
		mod_tags = []
		for tag in mod["tag"]:
			if SequenceMatcher(a=arg_mod, b=tag).ratio() > similarity:
				os.chdir(f"./modules/{mod['module']}")
				os.system(f"{config['modules'][mod_name]['runwith']} {mod['file']} {ar}")
				exit(0)
			mod_tags.append(f'[{tag}]')
		tags.append(" or ".join(mod_tags))

	descs = ""
	reg = "{" + f":{len(max(tags, key=len))}" + "}"

	for i in range(len(module_list)):
		mod = modules[module_list[i]]
		mod_name = reg.format(tags[i])
		descs += f"\n{mod_name}  :  {mod['description']}"

	if SequenceMatcher(a=arg_mod, b="help").ratio() > 0.7 or arg_mod == "h":
		print(f"""
use dav [module] <args>
use dav [edit] to edit the projects

MODULE LIST:
{descs}""")
	else:
		print(f"Unknown module \"{arg_mod}\"\n"
			  f"use dav [help] or [h]")


if __name__ == "__main__":
	main()
