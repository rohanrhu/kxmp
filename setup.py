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
 
from distutils.core import setup
from os import system

locales = []

translations = ["tr"] 
for i in translations:
    locales.append(("share/locale/%s/LC_MESSAGES" % i, ["kxmp/po/tr/LC_MESSAGES/kxmp.mo"]))

datas = [("share/applications", ["data/kxmp.desktop"]), ("share/pixmaps", ["kxmp/kxmp.png"])]

datas.extend(locales)

setup(name = "kxmp",
      version = "0.1.2",
      description = "Graphical xm player...",
      author = "Oğuzhan Eroğlu",
      author_email = "oguzhan@oguzhaneroglu.com",
      url = "http://kxmp.googlecode.com",
      packages = ["kxmp"],
      data_files = datas,
      scripts = ["data/kxmp"])