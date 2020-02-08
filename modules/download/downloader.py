# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Downloader
# Dav Project

import os

from sys import argv, exit
import sys
import platform
import subprocess
from tqdm import tqdm
import json

sys.path.append(f'{os.environ["USERPROFILE"]}\\dav-cli')
import dav


def main():
	# comment this line if dont get any errors!
	print("[WARNING]: You'll need FFmpeg installed for the mp3 conversion\n"
		  "check out -> http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ \n")

	# read config file
	config = dav.get_config()

	# Song Directory
	if not os.path.exists('Songs'):
		os.mkdir('Songs')
	else:
		os.chdir('Songs')

	args = list(map(str.lower, argv[1:]))

	if len(args) == 0:
		path = '../urllist.txt'

	elif args[0].endswith(".txt"):
		path = '../' + args[0]

	elif args[0] in ["file", "f"]:
		os.chdir('../')
		subprocess.Popen('urllist.txt', shell=True)
		exit(0)

	elif args[0] == 'move':
		os.chdir('..')
		os.system(f'{config["modules"]["download"]["runwith"]} move.py')
		exit(0)

	elif args[0] == 'edit':
		os.chdir('..')
		os.system(f'{config["text_editor"]} downloader.py')
		exit(0)
	elif args[0] in ["help", "h"]:
		print("""
	download <empty>    : start download from urllist.txt
	download file       : open urllist.txt file 
	download <file.txt> : download songs from given file
	download move       : move downloaded songs
	download edit       : edit script""")
		exit(0)
	else:
		print("file must be a .txt")
		exit(0)

	try:
		file = open(path, 'r')
	except:
		print("file not found :(")
		exit(0)

	lines = file.readlines()
	file.seek(0)

	if len(lines) == 0:
		print("file is empty!")
		print("use dl [file] and place your links")
		exit(0)

	print("Downloading...")

	# Download Songs
	try:
		for i in tqdm(range(len(lines))):
			url = lines[i].strip()
			# skip empty urls
			if not url: continue
			os.system(f'youtube-dl --extract-audio -q -x --audio-format mp3 {url}')
		open(path, 'w').close()
	except:
		print("ocorreu um erro no download")

	# move downloaded song
	os.chdir('..')
	os.system(f'{config["modules"]["download"]["runwith"]} move.py')


if __name__ == "__main__":
	main()
