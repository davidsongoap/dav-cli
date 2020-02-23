# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Module: Example
# Dav Project

# Feel free to use argparse
# or any parser you prefer

# imports
import os
import sys
from sys import argv
from sys import exit

sys.path.append(f'\"{os.environ["USERPROFILE"]}\\dav-cli\"')
from dav import get_config

def main():
	config = get_config()

	args = list(map(str.lower, argv[1:]))

	print("this is just a template.\n"
		  "customize it!")

if __name__ == '__main__':
    main()