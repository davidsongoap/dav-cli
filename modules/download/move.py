# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Move
# Dav Project

import os
import shutil
from sys import exit
import sys

sys.path.append(f'{os.environ["USERPROFILE"]}\\dav-cli')
import dav


def main():
	directory = "./Songs"

	# check if there are songs to move
	if len(os.listdir(directory)) == 0:
		print("Empty folder")
		exit(0)

	import numpy as np
	import json

	# read config file
	config = dav.get_config()

	artist_path = f'{os.environ["USERPROFILE"]}\\{config["modules"]["music"]["path"]}\\Artists'
	all_music_path = f'{os.environ["USERPROFILE"]}\\{config["modules"]["music"]["path"]}\\All Music'

	if not os.path.exists(all_music_path):
		os.system(f"mkdir {all_music_path}")
		print(f"created a folder for all the music")

	if not os.path.exists(artist_path):
		os.system(f"mkdir {artist_path}")
		print(f"created a folder for the artists")

	def get_artists():
		s = os.listdir(artist_path)
		artists = []
		for filename in s:
			if os.path.isdir(os.path.join(os.path.abspath(artist_path), filename)):
				artists.append(filename)
		artists.sort()
		artists = np.array(artists)
		return artists

	# all artists with a folder
	artists = get_artists()
	if len(artists):
		artists = np.char.lower(artists)

	def handle_name(original_name):
		s = np.array(list(original_name))
		t = np.where(s == '-')
		if len(t[0]) > 1:
			s = s[0:t[0][-1]]
			final_name = "".join(list(s)).strip() + ".mp3"
		elif len(t[0]) == 1:
			s = s[0:t[0][0]]
			final_name = "".join(list(s)).strip() + ".mp3"
		else:
			final_name = "".join(list(s))

		# text to be removed from the title
		# TODO use regular expression somehow
		final_name = final_name.replace('(Official Audio)', '')
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
		name = name.strip()
		s = np.array(list(name))
		t = np.where(s == '-')
		if (len(t[0]) > 0):
			s = s[:t[0][0]]
			if (s[-1] == ' '): s = s[:-1]
		artist = "".join(s)
		if len(artists) > 0:
			x = np.where(artists == artist.lower())
		else:
			x = [[]]
		try:
			if (len(x[0]) > 0):
				# artist already has a folder, puts the song there
				shutil.copy(f"{directory}\\{name}", f"{artist_path}{artists[x[0][0]]}")
			else:
				# creates a folder for the artist
				print(f"Created a folder for the artist: {artist}")
				os.mkdir(f'{artist_path}\\{artist}')
				shutil.copy(f"{directory}\\{name}", f'{artist_path}\\{artist}')

			# move song to phone folder
			shutil.move(f"{directory}\\{name}", all_music_path)
			print(f"{name} has been added to the library.")
		except:
			print(f"{name} already exists in the library!")

	print("Moving...")
	for filename in os.listdir(directory):
		if filename.endswith(".mp3"):
			# format song name
			new_name = handle_name(filename)
			# move song
			move_file(new_name)


if __name__ == '__main__':
	main()
