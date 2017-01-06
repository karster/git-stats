#!/usr/bin/env python
# UTF-8 coding
#  -*- coding: utf-8 -*-
# 
# Script Name		: git-keyword-stats.py
# Author			: Ing. Lukas Hrdlicka
# Created			: 15th November 2016
# Last Modified		: 6th January 2017
# Version			: 1.0
# Description		: This simple script parse git log and create statistics acording to keywords

import argparse
import subprocess
import re
import json
import os
from texttable import Texttable
from GitParser import GitParser
from StringIO import StringIO

parser = argparse.ArgumentParser(prog="git-keyword-stats")

parser.add_argument('--include-merges' , help="Look at merge commits", action="store_true")
parser.add_argument('--since', help="Log since <date>", metavar="<date>")
parser.add_argument('--until', help="Log until <date>", metavar="<date>")
parser.add_argument('--before', help="Log before <date>", metavar="<date>")
parser.add_argument('--after', help="Log after <date>", metavar="<date>")
parser.add_argument('--last-month', help="Log since 1 month ago", action="store_true")
parser.add_argument('--last-week', help="Log since 1 week ago", action="store_true")
parser.add_argument('--keywords-path', help="Set path to file with keywords in json format", metavar="<path>")
parser.add_argument('--save-file-path', help="Path to file", metavar="<path>")

args = parser.parse_args()

git_merges = ""
git_date   = ""
filepath   = ""

if args.keywords_path:
	dir_path = args.keywords_path
else:
	dir_path = os.path.dirname(os.path.realpath(__file__)) + '/default-keywords.json'
	
with open(dir_path) as data_file:    
	keywords = json.load(data_file)

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

for package in packages:

	if not package.author in stats:
		stats[package.author] = {}
		for keyword in keywords:
			stats[package.author][keyword] = 0

	for keyword in keywords:
		if bool(re.search(keyword, package.message, re.IGNORECASE)):
			stats[package.author][keyword] += 1


table      = Texttable()
header     = ['Author / keyword']
col_width  = ["50"]
col_align  = ["l"]

for keyword in keywords:
	header.append(keyword)
	col_width.append("10")
	col_align.append("c")

table.set_cols_align(col_align)
table.set_cols_width(col_width)
table.add_rows([header])

for index, author in enumerate(stats):
	row = [author]
	for keyword in keywords:
		row.append(stats[author][keyword])

	table.add_rows([row], False)	
	
if filepath:
	file = open(filepath, 'a')
	print >> file, table.draw().encode('utf-8').strip() + "\n"
	file.close()
else:
	print table.draw() + "\n"
