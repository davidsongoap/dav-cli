# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Fun
# Dav Project

# imports
import os
from sys import exit
from sys import argv


def main():
	args = list(map(str.lower, argv[1:]))

	if len(args) == 0:
		print("no item selected :(")
		exit(0)

	elif args[0] == "joke":
		os.system(f'curl -H "Accept: text/plain" https://icanhazdadjoke.com/')


if __name__ == '__main__':
	main()
