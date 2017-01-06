#!/usr/bin/env python
# UTF-8 coding
#  -*- coding: utf-8 -*-
# 
# Script Name		: git-author-stats.py
# Author			: Ing. Lukas Hrdlicka
# Created			: 13th November 2016
# Last Modified		: 6th January 2017
# Version			: 1.0
# Description		: This simple script parse git log and create statistics

import argparse
import subprocess
from texttable import Texttable
from GitParser import GitParser

parser = argparse.ArgumentParser(prog="git-author-stats")

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

files_name    = 'files'
inserted_name = 'inserted'
deleted_name  = 'deleted'
commits_name  = 'commits'

for package in packages:

	if not package.author in stats:
		stats[package.author] = {
			files_name: 0,
			inserted_name: 0,
			deleted_name: 0,
			commits_name: 0
		}

	stats[package.author][files_name] += int(package.files)
	stats[package.author][commits_name] += int(package.commits)
	stats[package.author][inserted_name] += float(package.inserted)
	stats[package.author][deleted_name] += float(package.deleted)	

table = Texttable()
table.set_cols_align(["l", "c", "c", "c", "c", "c", "c"])
table.set_cols_width(["50", "10", "20", "20", "20", "10", "20"])
table.add_rows([["Author", "Commits", "Files changed", "Insertions (+)", "Deletions (-)", "Delta", "Ratio [1 : n]"]])

for index, author in enumerate(stats):
	
	ratio_text = '-'
	if stats[author][inserted_name]:
		ratio_tmp = '%.2f' % float(stats[author][deleted_name] / stats[author][inserted_name])
		ratio_text = "1 : " + str(ratio_tmp)

	table.add_rows([[
		author, 
		int(stats[author][commits_name]), 
		int(stats[author][files_name]), 
		int(stats[author][inserted_name]), 
		int(stats[author][deleted_name]), 
		int(stats[author][inserted_name] - stats[author][deleted_name]), 
		ratio_text
	]], False)
	
if filepath:
	file = open(filepath, 'a')
	print >> file, table.draw().encode('utf-8').strip() + "\n"
	file.close()
else:
	print table.draw() + "\n"
