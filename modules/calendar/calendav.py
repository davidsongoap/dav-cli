# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Class: Calendar
# Dav Project

import json
from datetime import datetime
import calendar
import colorama
colorama.init()


class Calendar:
	def __init__(self, event_file, config_file):
		"""
		:param event_file: str
		:param config_file: str
		"""
		self.event_file = event_file
		self.config_file = config_file
		self.events = self.load_json(event_file)
		self.config = self.load_json(config_file)
		self.today = datetime.today()

	def update_event_file(self):
		"""
		Updates the event file with the added and/or removed event
		:return: None
		"""
		with open(self.event_file, 'w') as outfile:
			json.dump(self.events, outfile, indent=2, sort_keys=True)
		outfile.close()

	def load_json(self, path):
		"""
		Loads a json file
		:param path: str
		:return: dict
		"""
		# read config file
		with open(path, 'r') as file:
			read_data = file.read()
		file.close()
		return json.loads(read_data)

	def get_event_dates(self):
		"""
		Returns all the dates from the events
		Stores them as tuples: (eventID, eventDate)
		:return: list
		"""
		date_list = []
		for ev in self.events:
			ev_id = ev["id"]
			ev_date = datetime(day=int(ev["day"]), month=int(ev["month"]), year=int(ev["year"]),
							   hour=23, minute=59, second=59)
			date_list.append((ev_id, ev_date))
		return date_list

	def get_events_after_today(self, date_list):
		"""
		Returns all of the events after the currennt date
		:param date_list: list
		:return: list
		"""
		dates_after_today = []
		for i in range(len(date_list)):
			if date_list[i][1] >= self.today:
				dates_after_today.append(date_list[i][1])
		return dates_after_today

	def nearest_events(self):
		"""
		Return the date of the nearest event(s)
		Return (None,None) if there are no near events
		:return: tuple
		"""
		date_list = self.get_event_dates()
		dates_after_today = self.get_events_after_today(date_list)
		try:
			min_date = min(dates_after_today,
						   key=lambda x: abs(x - self.today))
			ids = []
			# get the ids of the events on this date
			for i in date_list:
				if i[1] == min_date:
					ids.append(i[0])
			return (min_date, ids)
		except:
			return (None, None)

	def print_near_events(self):
		"""
		Print near events
		:return: None
		"""
		nearest_date, ids = self.nearest_events()

		if nearest_date == None:
			print("No events soon.")
			return

		d = str(nearest_date.day).zfill(2)
		m = str(nearest_date.month).zfill(2)
		y = str(nearest_date.year).zfill(2)
		closest_date = f"{d}/{m}/{y}"

		# get description of all events on the closest date
		desc = []
		for id in ids:
			for ev in self.events:
				if ev["id"] == id:
					desc.append(ev["description"])

		# show events
		print("Next event at:")
		for i in desc:
			print(f"{closest_date} - {i}")

	def clear(self):
		"""
		Clears the calendar after confirmation
		:return: None
		"""
		c = input("Are you sure you want to clear the calendar? [Y/n] \n")
		if c == "Y":
			s = input("Write \"yes\" to erase everything \n")
			if s == "yes":
				self.events = []
				with open('events.json', 'w') as outfile:
					json.dump(self.events, outfile, indent=2, sort_keys=True)
				self.update_event_file()
		print("Calendar clear was cancelled")

	def get_current_month_events(self, dates):
		month_dates = []
		for id, date in self.get_event_dates():
			if date.month == self.today.month:
				month_dates.append(date)
		return month_dates

	def get_current_month(self):
		"""
		Returns current month as string
		With the events colored
		:return: str
		"""
		month_str = calendar.month(self.today.year, self.today.month, 4, 2)
		dates = self.get_current_month_events(self.get_event_dates())

		month_str = month_str.replace(f' {self.today.day}',
									  f' \033[92m{self.today.day}\033[0m')

		for date in dates:
			if date.day != self.today.day:
				month_str = month_str.replace(f' {date.day}',
											  f' \033[93m{date.day}\033[0m')
			else:
				month_str = month_str.replace(
					f'\033[92m{self.today.day}\033[0m',
					f'\033[91m{date.day}\033[0m')
		month_str = month_str.replace(f'{self.today.year}',
									  f'\033[97m{self.today.year}\033[0m')
		return month_str

	def get_events_max_id(self):
		"""
		Return highest event
		:return: int
		"""
		try:
			return self.events[-1]["id"]
		except:
			return 1

	def print_current_month(self):
		"""
		Print the current month
		:return: None
		"""
		print("\n"+self.get_current_month(), end=" ")

	def get_current_year(self):
		"""
		Returns current year as string
		:return: str
		"""
		return calendar.calendar(datetime.today().year, 2, 1)

	def print_current_year(self):
		"""
		Print the current year
		:return: None
		"""
		print(self.get_current_year())

	def remove_event(self, idx):
		"""
		Removes the event at the given index
		:param idx: int
		:return: None
		"""
		try:
			# validate event number
			rem_idx = int(idx)
			# remove event
			ev = self.events.pop(rem_idx - 1)
			print(f'Event: {ev["description"]} was removed')
			self.update_event_file()
		except:
			print("Invalid event")

	def add_event(self):
		"""
		Adds an event to the calendar
		:return: None
		"""
		# inputs
		current_year = self.today.year
		day = input("day: ").strip()
		month = input("month: ").strip()
		year = input(f"year({current_year}): ").strip()

		# assumes as the current year if no year is provided
		if not year:
			year = current_year
		new_desc = input("Description: ").strip()
		id = self.get_events_max_id() + 1

		try:
			# date validation
			new_ev_date = datetime(
				day=int(day), month=int(month), year=int(year))

			# create event
			new_event = {
				"day": day,
				"month": month,
				"year": year,
				"description": new_desc,
				"id": id
			}

			# add event
			self.events.append(new_event)
			self.update_event_file()
		except:
			print("Invalid Date!")
			print(f"Failed to add event: {new_desc}")

	def __str__(self):
		"""
		Calendar events string
		:return: str
		"""
		if len(self.events) == 0:
			return "No events. Use calendar [add]"
		cal_str = ""
		for i in range(len(self.events)):
			ev = self.events[i]
			cal_str += f'\n{str(i + 1).zfill(2)}. {str(ev["day"]).zfill(2)}/{str(ev["month"]).zfill(2)}/' \
				f'{ev["year"]} - {ev["description"]} '
		return cal_str

	def print_events(self):
		"""
		print Calendar events string
		:return: None
		"""
		print(str(self))
