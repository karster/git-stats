#!/usr/bin/env python
# UTF-8 coding
#  -*- coding: utf-8 -*-
# 
# Script Name		: git-activity-stats.py
# Author			: Ing. Lukas Hrdlicka
# Created			: 6th January 2017
# Last Modified		: 6th January 2017
# Version			: 1.0
# Description		: This simple script parse git log and create statistics

import argparse
import subprocess
from texttable import Texttable
from GitParser import GitParser
from dateutil.parser import parse as dateparser

parser = argparse.ArgumentParser(prog="git-activity-stats")

parser.add_argument('--include-merges' , help="Look at merge commits", action="store_true")
parser.add_argument('--since', help="Log since <date>", metavar="<date>")
parser.add_argument('--until', help="Log until <date>", metavar="<date>")
parser.add_argument('--before', help="Log before <date>", metavar="<date>")
parser.add_argument('--after', help="Log after <date>", metavar="<date>")
parser.add_argument('--last-month', help="Log since 1 month ago", action="store_true")
parser.add_argument('--last-week', help="Log since 1 week ago", action="store_true")
parser.add_argument('--save-file-path', help="Path to file", metavar="<path>")

args = parser.parse_args()

git_merges = ""
git_date   = ""
filepath   = ""

if not args.include_merges:
	git_merges = '--no-merges'

if args.since:
	git_date = '--since=' + args.since

if args.until:
	git_date = '--until=' + args.until

if args.before:
	git_date = '--before=' + args.before

if args.after:
	git_date = '--after=' + args.after

if args.last_month:
	git_date = '--since=1 month ago'

if args.last_week:
	git_date = '--since=1 week ago'

if args.save_file_path:
	filepath = args.save_file_path

git_arguments = filter(None, ['git', 'log', '--shortstat', git_merges, git_date])
git_output    = subprocess.check_output(git_arguments)

git_parser = GitParser(git_output)
packages   = git_parser.run()

stats = {}

days  	 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
hours    = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_days_list():
	return {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0, "29": 0, "30": 0, "31": 0}

def get_hours_list():
	return {"00": 0, "01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0}

def get_wekkdays_list():
	return {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}

for package in packages:
	
	date_object = dateparser(package.date)

	day_of_week  = date_object.strftime("%A")
	hour_of_day  = date_object.strftime("%H")
	day_of_month = date_object.strftime("%d")

	if not package.author in stats:
		stats[package.author] = {
			"hour_of_day": get_hours_list(),
			"day_of_week": get_wekkdays_list(),
			"day_of_month": get_days_list(),
			"hour_of_week": {
				"Monday": get_hours_list(),
				"Tuesday": get_hours_list(),
				"Wednesday": get_hours_list(),
				"Thursday": get_hours_list(),
				"Friday": get_hours_list(),
				"Saturday": get_hours_list(),
				"Sunday": get_hours_list()
			}
		}

	stats[package.author]['day_of_week'][day_of_week] += 1
	stats[package.author]['hour_of_day'][hour_of_day] += 1
	stats[package.author]['day_of_month'][day_of_month] += 1
	stats[package.author]['hour_of_week'][day_of_week][hour_of_day] += 1

	
empty_values = ""

if filepath:
	file = open(filepath, 'a')

table = Texttable()
table.set_cols_align(["l", "c", "c", "c", "c", "c", "c", "c"])
table.set_cols_width(["50", "10", "10", "10", "10", "10", "10", "10"])
table.add_rows([["Author / Weekdays", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]])

for index, author in enumerate(stats):
	
	row = [author]

	for weekday in weekdays:
		commit_count = int(stats[author]['day_of_week'][weekday])

		if commit_count == 0:
			row.append(empty_values)
		else:
			row.append(commit_count)

	table.add_rows([row], False)	

if filepath:
	print >> file, table.draw().encode('utf-8').strip() + "\n"
else:
	print table.draw() + "\n"


table 	  = Texttable()
header 	  = ["Author / Hours"]
col_width = ["50"]
col_align = ["l"]

for hour in hours:
	header.append(hour)
	col_width.append("2")
	col_align.append("c")

table.set_cols_width(col_width)
table.set_cols_align(col_align)
table.add_rows([header])

for index, author in enumerate(stats):
	
	row = [author]

	for hour in hours:
		commit_count = int(stats[author]['hour_of_day'][hour])

		if commit_count == 0:
			row.append(empty_values)
		else:
			row.append(commit_count)

	table.add_rows([row], False)
	

if filepath:
	print >> file, table.draw().encode('utf-8').strip() + "\n"
else:
	print table.draw() + "\n"


table 	  = Texttable()
header 	  = ["Author / Days"]
col_width = ["50"]
col_align = ["l"]

for day in days:
	header.append(day)
	col_width.append("2")
	col_align.append("c")

table.set_cols_width(col_width)
table.set_cols_align(col_align)
table.add_rows([header])

for index, author in enumerate(stats):
	
	row = [author]

	for day in days:
		commit_count = int(stats[author]['day_of_month'][day])

		if commit_count == 0:
			row.append(empty_values)
		else:
			row.append(commit_count)

	table.add_rows([row], False)
	

if filepath:
	print >> file, table.draw().encode('utf-8').strip() + "\n"
else:
	print table.draw() + "\n"


for index, author in enumerate(stats):
	
	if filepath:
		print >> file, author
	else:
		print author

	table 	  = Texttable()
	header 	  = ["Weekdays / Hours"]
	col_width = ["50"]
	col_align = ["c"]

	for hour in hours:
		header.append(hour)
		col_width.append("2")
		col_align.append("c")

	table.set_cols_width(col_width)
	table.set_cols_align(col_align)
	table.add_rows([header])

	for weekday in weekdays:

		row = [weekday]

		for hour in hours:

			commit_count = int(stats[author]['hour_of_week'][weekday][hour])

			if commit_count == 0:
				row.append(empty_values)
			else:
				row.append(commit_count)

		table.add_rows([row], False)
	
	if filepath:
		print >> file, table.draw().encode('utf-8').strip() + "\n"
	else:
		print table.draw() + "\n"


if filepath:
	file.close()

