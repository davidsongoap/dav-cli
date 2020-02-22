# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Author: Davidson Gonçalves
# Module: Email
# Dav Project

import email
import getpass
import imaplib
from email.header import decode_header, make_header
from sys import argv as args
from sys import exit
import json
import os
import sys

import colorama
colorama.init()

sys.path.append(f'{os.environ["USERPROFILE"]}\\dav-cli')
from dav import get_config


def main():
	# comment this line if dont get any errors!
	print("\033[93m[WARNING]: Don't forget to allow access to Less Secure Apps in your email settings.\n\033[0m")

	argv = list(map(str.lower, args[1:]))

	# read config file
	config = get_config()

	if argv[0] == "g":
		service = ".gmail"
		user = config["modules"]["gmail"]["emailadd"]
	else:
		service = "-mail.outlook"
		user = config["modules"]["hotmail"]["emailadd"]

	box = 'unseen'
	n_read = 5

	def valArg(arg):
		global box
		global n_read
		try:
			n_read = int(arg)
		except:
			if arg == 'all':
				box = 'all'
			elif arg == 'edit':
				os.system(f"{config['text_editor']} myemail.py")
			return

	if len(argv) >= 2:
		for i in range(1, len(argv)):
			try:
				valArg(argv[i])
			except:
				pass

			if argv[i] == 'edit':
				exit(0)
			elif argv[i] in ["help", "h"]:
				print("""
mail <empty>    : show 5 unread emails
mail [all]      : show all emails (read or unread)
mail <number>   : show <n> emails """)
				exit(0)

	print(f"Email: {user}")
	auth = True
	while auth:
		pwd = getpass.getpass("Enter your password: ")
		try:
			# connecting to the gmail/hotmail imap server
			m = imaplib.IMAP4_SSL(f"imap{service}.com")
		except:
			print("Connection Error :(")
			exit(0)
		try:
			m.login(user, pwd)
			auth = False
		except:
			print("\nIncorrect Password")

	m.select("Inbox")

	resp, mail_ids = m.search(None, box)

	# getting the emails id
	mail_ids = (mail_ids[0].split()[-n_read:])[::-1]
	print()

	msgs = []
	ns = 30
	print(f"{'-' * ns} INBOX ({box}) {'-' * ns}")

	# loop over (n) emails
	for z in range(len(mail_ids)):
		i = mail_ids[z]
		print(f"\n{str(z + 1).zfill(2)}.")
		# decode the emails
		typ, msg_data = m.fetch(i.decode(), '(RFC822)')
		for response_part in msg_data:
			if isinstance(response_part, tuple):
				msg = email.message_from_string(
					response_part[1].decode('iso-8859-1'))
				msgs.append(msg)
				from_m = make_header(decode_header(msg['from']))
				date = make_header(decode_header(msg['Date']))
				subj = make_header(decode_header(msg['Subject']))
				print(f"FROM: {from_m} \n"
					  f"SUBJECT: {subj}\n"
					  f"DATE: {str(date)[:-5]}")
	m.close()
	print(f"{'-' * ns}----------------{'-' * ns}")


if __name__ == '__main__':
	main()
