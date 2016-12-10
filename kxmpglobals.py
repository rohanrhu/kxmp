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
import sys
from PyKDE4.kdecore import ki18n, KAboutData

import gettext
import locale

local, encoding = locale.getdefaultlocale()

_ = gettext.translation("kxmp", fallback=True, languages=[local]).ugettext
__ = gettext.translation("kxmp", fallback=True, languages=[local]).gettext

versionStatus = "beta2"

appName = "KXmp"
catalog = ""
programName = ki18n("KXmp")
version = "0.1.2"
description = ki18n(__("KXmp is graphical cracktro player for KDE4..."))
license = KAboutData.License_GPL
copyright = ki18n("(c) 2008 Oğuzhan Eroğlu")
text = ki18n("")
homePage = "http://kxmp.googlecode.com"
bugEmail = "rohanrhu2@gmail.com"