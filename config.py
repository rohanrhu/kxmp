# -*- coding: utf-8 -*-
# KXmp is a xm media player for KDE4
 # Copyright (C) 2008, Oğuzhan Eroğlu <rohanrhu2@gmail.com>
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.

 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.

import os
import shelve

dbPath = "%s/.kxmp.db" % os.getenv("HOME")

allConfigs = ["path", "isIgnoreCase", "isShuffle", "isColored"]

if not os.path.exists(dbPath):
	isFirst = True
else:
	isFirst = False

def openDb():
	global db
	db = shelve.open(dbPath)

def setPath(path):
	openDb()
	db["path"] = path
	db.close()

def setIgnoreCase(isCase):
	openDb()
	db["isIgnoreCase"] = isCase
	db.close()

def setColored(color):
	openDb()
	db["isColored"] = color
	db.close()

def setShuffle(shuffle):
	openDb()
	db["isShuffle"] = shuffle
	db.close()

def first():
	print "..."
	openDb()
	db["path"] = ""
	db["isIgnoreCase"] = False
	setColored(True)
	setShuffle(False)
	db.close()

if isFirst:
	first()
else:
	db_ = shelve.open(dbPath)

	try:
		for i in allConfigs:
			db_[str(i)]
	except:
		first()

	db_.close()