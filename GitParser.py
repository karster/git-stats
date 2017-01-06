#!/usr/bin/env python
# UTF-8 coding
#  -*- coding: utf-8 -*-
# 
# GitParser

import cStringIO
import re

class GitParser:

	def __init__(self, strem):
		self.fake_file = cStringIO.StringIO(strem)
		self.commits   = []

	def run(self):

		commit = GitCommit()
		
		for line in self.fake_file:
			if line == '' or line == '\n':
				pass

			elif bool(re.match('commit', line, re.IGNORECASE)):
				
				if commit.commits:
					self.commits.append(commit)
					commit = GitCommit()

				commit.parseHash(line)

			elif bool(re.search('merge:', line, re.IGNORECASE)):
				commit.parseMerge(line)
				
			elif bool(re.match('author:', line, re.IGNORECASE)):
				commit.parseAuthor(line)

			elif bool(re.match('date:', line, re.IGNORECASE)):
				commit.parseDate(line)
				
			elif bool(re.search('    ', line, re.IGNORECASE)):
				commit.parseCommitMessage(line)

			elif bool(re.search('fil(e|es) changed', line, re.IGNORECASE)):
				commit.parseFileMessage(line)

			else:
				print ('ERROR: Unexpected Line: ' + line)

		if commit.commits:
			self.commits.append(commit)
			commit = {}

		return self.commits


# Git Commit
class GitCommit():
	def __init__(self):
		self.files    = 0
		self.inserted = 0
		self.deleted  = 0
		self.commits  = 0
		self.message  = ""
		self.date     = ""
		self.author   = ""
		self.email    = ""
		self.name     = ""
		self.hash     = ""

	def parseFileMessage(self, line):

		files_regex = '(\d+) fil(e|es) changed'
		if bool(re.search(files_regex, line)):
			self.files = re.search(files_regex, line).group(1)

		inserted_regex = '(\d+) insert'
		if bool(re.search(inserted_regex, line)):
			self.inserted = re.search(inserted_regex, line).group(1)

		deleted_regex = '(\d+) delet'
		if bool(re.search(deleted_regex, line)):
			self.deleted = re.search(deleted_regex, line).group(1)

	def parseDate(self, line):
		self.date = re.match('Date: (.*)', line).group(1).strip()

	def parseCommitMessage(self, line):
		self.message = line.strip()			

	def parseAuthor(self, line):
		author = re.match('Author: (.*) <(.*)>', line)
		self.name   = author.group(1)
		self.email  = author.group(2)
		self.author = self.name+" <"+self.email+">"

	def parseMerge(self, line):
		self.merge = re.match('merge: (.*)', line, re.IGNORECASE).group(1).strip()

	def parseHash(self, line):
		self.hash    = re.match('commit (.*)', line, re.IGNORECASE).group(1)
		self.commits = 1