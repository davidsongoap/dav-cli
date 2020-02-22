# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Calendar
# Dav Project

# imports
import os
from sys import argv
from calendav import Calendar

def main():
	args = list(map(str.lower, argv[1:]))

	ev_path = "events.json"
	config_path = "../../config/config.json"
	cal = Calendar(ev_path, config_path)

	if (len(args) == 0):
		cal.print_events()

	elif args[0] == "next":
		cal.print_near_events()

	elif args[0] == "clear":
		cal.clear()

	elif args[0] in ["month", "m"]:
		cal.print_current_month()

	elif args[0] in ["year", "y"]:
		cal.print_current_year()

	elif args[0] in ["rem", "remove"]:
		try:
			cal.remove_event(int(args[1]))
		except:
			print("No event provided")

	elif args[0] in ["file", "f"]:
		os.system(f"{cal.config['text_editor']} events.json")

	elif args[0] == "add":
		cal.add_event()

	elif args[0] == "edit":
		os.system(f"{cal.config['text_editor']} calendav.py")

	elif args[0] in ["help", "h"]:
		print("""
calendar <empty>              : show full calendar
calendar [next]               : show next event
calendar [add]                : add event
calendar [rem] <event number> : remove the event of the given number
calendar [clear]              : clear calendar
calendar [year]               : open current year calendar
calendar [month]              : open current month calendar
calendar [file]               : open calendar json files
calendar [edit]               : edit script""")

	else:
		print("Invalid argument use calendar [h] for help")


if __name__ == "__main__":
	main()
