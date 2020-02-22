# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Downloader
# Dav Project

# imports
from dav import get_config
import os
from sys import argv, exit
import sys
import subprocess
from tqdm import tqdm
import colorama
colorama.init()
sys.path.append(f'{os.environ["USERPROFILE"]}\\dav-cli')

# read config file
config = get_config()


def main():
	# comment this line if dont get any errors!
	print("\033[93m[WARNING]: You'll need FFmpeg installed for the mp3 conversion\n"
		  "check out -> http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ \n\033[0m")

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
	download <empty>      : start download from urllist.txt
	download [file]       : open urllist.txt file 
	download <file.txt>   : download songs from given file
	download [move]       : move downloaded songs
	download [edit]       : edit script""")
		exit(0)
	else:
		print("file must be a .txt")
		exit(0)
	download_songs(path)


def download_songs(path):
	try:
		with open(path) as file:
			# read data
			lines = file.readlines()
			file.seek(0)
	except:
		print("file not found :(")
		exit(0)

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
			if not url:
				continue
			os.system(
				f'youtube-dl --extract-audio --output "%(title)s.%(ext)s" -q -x --audio-format mp3 {url}')

		# clear the file
		open(path, 'w').close()
		move_songs()
	except:
		print("ocorreu um erro no download")


def move_songs():
	# move downloaded song
	os.chdir('..')
	os.system(f'{config["modules"]["download"]["runwith"]} move.py')


if __name__ == "__main__":
	main()
