# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Move
# Dav Project

# imports
import os
import shutil
from sys import exit
import sys
import numpy as np
import colorama
colorama.init()

sys.path.append(f'{os.environ["USERPROFILE"]}\\dav-cli')
from dav import get_config

# read config file
config = get_config()
directory = "./Songs"
artist_path = f'{os.environ["USERPROFILE"]}\\{config["modules"]["music"]["path"]}\\Artists'
all_music_path = f'{os.environ["USERPROFILE"]}\\{config["modules"]["music"]["path"]}\\All Music'


def get_artists():
	s = os.listdir(artist_path)
	artists = []
	for filename in s:
		if os.path.isdir(os.path.join(os.path.abspath(artist_path), filename)):
			artists.append(filename)
	artists.sort()
	artists = np.array(artists)
	return artists


def handle_name(original_name):
	# all artists with a folder
	artists = get_artists()
	if len(artists):
		artists = np.char.lower(artists)
	# text to be removed from the title
	# TODO use regular expression somehow
	final_name = original_name.replace('(Official Audio)', '')
	final_name = final_name.replace('(Official Music Video)', '')
	final_name = final_name.replace('[Official Audio]', '')
	final_name = final_name.replace('[Official Video]', '')
	final_name = final_name.replace('[Official Video]', '')
	final_name = final_name.replace('[OFFICIAL AUDIO]', '')
	final_name = final_name.replace('(official audio)', '')
	final_name = final_name.replace('(official video)', '')
	final_name = final_name.replace('(Lyrics Video)', '')
	final_name = final_name.replace('(Lyrics)', '')
	final_name = final_name.replace('lyrics', '')
	final_name = final_name.replace('(LYRICS)', '')
	final_name = final_name.replace('Lyrics', '')
	final_name = final_name.replace('(lyrics)', '')
	final_name = final_name.replace('[Monstercat Release]', '')
	final_name = final_name.replace('[Explicit]', '')
	final_name = final_name.replace('(Official MusicVideo)', '')
	final_name = final_name.replace('(Legendado)', '')
	final_name = final_name.replace('[CC]', '')
	final_name = final_name.replace('(HQ)', '')
	final_name = final_name.replace('[HQ]', '')
	final_name = final_name.replace('[HD]', '')
	final_name = final_name.replace('(HD)', '')
	final_name = final_name.replace('(Audio)', '')
	final_name = final_name.replace('(audio)', '')

	# rename the song
	os.rename(f"{directory}\\{original_name}", f"{directory}\\{final_name}")
	return final_name


def move_file(name):
	artists = get_artists()
	name = name.strip()
	s = np.array(list(name))
	t = np.where(s == '-')
	if (len(t[0]) > 0):
		s = s[:t[0][0]]
		if (s[-1] == ' '):
			s = s[:-1]
	artist = "".join(s)
	if len(artists) > 0:
		x = np.where(artists == artist.lower())
	else:
		x = [[]]
	try:
		if (len(x[0]) > 0):
			# artist already has a folder, puts the song there
			shutil.copy(f"{directory}\\{name}",
						f"{artist_path}\\{artists[x[0][0]]}")
		else:
			# creates a folder for the artist
			print(f"Created a folder for the artist: {artist}")
			os.mkdir(f'{artist_path}\\{artist}')
			shutil.copy(f"{directory}\\{name}", f'{artist_path}\\{artist}')
		# move song to phone folder
		shutil.move(f"{directory}\\{name}", all_music_path)
		print(f"\033[92m{name} has been added to the library.\033[0m")
	except:
		print(f"\033[93{name} already exists in the library!\033[0m")


def main():
	# check if there are songs to move
	if len(os.listdir(directory)) == 0:
		print("Empty folder")
		exit(0)

	# create folders if needed
	if not os.path.exists(all_music_path):
		os.system(f"mkdir {all_music_path}")
		print(f"created a folder for all the music")

	if not os.path.exists(artist_path):
		os.system(f"mkdir {artist_path}")
		print(f"created a folder for the artists")

	print("Moving...")
	for filename in os.listdir(directory):
		if filename.endswith(".mp3"):
			# format song name
			new_name = handle_name(filename)
			# move song
			move_file(new_name)


if __name__ == '__main__':
	main()
