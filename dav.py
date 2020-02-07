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
use dav <module> <args>
or dav [h] for help""")
		exit(0)

	argv = list(map(str.lower, argv))
	arg_mod = argv[0]
	ar = " ".join(argv[1:])

	similarity = 0.8

	module_dict = {}
	module_list = []
	config = get_config()

	modules = config["modules"]
	tags = []

	for i in list(modules.keys()): module_list.append(i)

	for i in module_list:
		mod = modules[i]
		for j in mod["tag"]:
			module_dict[j] = (mod["file"], mod["module"], i)
			tags.append(j)

	for tag in tags:
		if SequenceMatcher(a=arg_mod, b=tag).ratio() > similarity:
			os.chdir(f"./modules/{module_dict[tag][1]}")
			os.system(f"{config['modules'][module_dict[tag][2]]['runwith']} {module_dict[tag][0]} {ar}")
			exit(0)

	descs = ""
	reg = "{" + f":{len(max(module_list, key=len))}" + "}"

	for i in module_list:
		mod = modules[i]
		mod_name = reg.format(i)
		descs += f"\n{mod_name}  :  {mod['description']}"
	if SequenceMatcher(a=arg_mod, b="help").ratio() > 0.7 or arg_mod == "h":
		print(f"""
use dav <module> <args>
or use dav [edit] to edit the projects

MODULE LIST:
{descs}""")

	else:
		print(f"Unknown module \"{arg_mod}\"")


if __name__ == "__main__":
	main()
