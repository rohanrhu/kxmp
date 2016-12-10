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

from PyQt4 import QtCore, QtGui
from PyKDE4.kdecore import KAboutData, KCmdLineArgs, ki18n, KGlobal
from PyKDE4.kdeui import KApplication, KAboutApplicationDialog, KSystemTrayIcon

import os
import sys
import subprocess
import re
from random import shuffle
import gettext
import locale

from ui_kxmp import Ui_kxmpWindow
from ui_config import Ui_configWindow
from kxmpglobals import *

import shelve
import config

local, encoding = locale.getdefaultlocale()

_ = gettext.translation("kxmp", fallback=True, languages=[local]).ugettext
__ = gettext.translation("kxmp", fallback=True, languages=[local]).gettext

if not os.path.exists("/usr/bin/xmp"):
	print _("xmp command is not installed, please install...")
	sys.exit()

class configWindow(Ui_configWindow, QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)

		self.connect(self.buttons, QtCore.SIGNAL("accepted()"), self.accept)
		self.connect(self.buttons, QtCore.SIGNAL("rejected()"), self.reject)
		self.connect(self.dirSelectButton, QtCore.SIGNAL("clicked(bool)"), self.selectDir)

		self.db = shelve.open("%s/.kxmp.db" % os.getenv("HOME"))
		path = self.db["path"]
		isCase = self.db["isIgnoreCase"]
		isShuffle = self.db["isShuffle"]
		isColored = self.db["isColored"]

		self.pathLine.setText(path)
		if isShuffle:
			self.isShuffle.setCheckState(QtCore.Qt.Checked)
		else:
			self.isShuffle.setCheckState(QtCore.Qt.Unchecked)

		if isColored:
			self.isColored.setCheckState(QtCore.Qt.Checked)
		else:
			self.isColored.setCheckState(QtCore.Qt.Unchecked)

		if isCase:
			self.isIgnoreCase.setCheckState(QtCore.Qt.Checked)
		else:
			self.isIgnoreCase.setCheckState(QtCore.Qt.Unchecked)

		self.db.close()

	def selectDir(self):
		self.dir = QtGui.QFileDialog.getExistingDirectory(self, _(u"Change to musics dir"), str(os.environ["HOME"]))
		self.dir = unicode(self.dir)

		self.pathLine.setText(self.dir)

	def accept(self):
		config.setIgnoreCase(self.isIgnoreCase.isChecked())

		config.setShuffle(self.isShuffle.isChecked())
		config.setColored(self.isColored.isChecked())

		path = unicode(self.pathLine.text())
		config.setPath(path)
		self.done(0)

	def reject(self):
		self.done(0)

class mainWindow(Ui_kxmpWindow, QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setupUi(self)

		screen = QtGui.QDesktopWidget().screenGeometry()
		size =  self.geometry()
		self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

		self.connect(self.playButton, QtCore.SIGNAL("clicked(bool)"), self.play)
		self.connect(self.stopButton, QtCore.SIGNAL("clicked(bool)"), self.stop)
		self.connect(self.actionPlay, QtCore.SIGNAL("triggered(bool)"), self.play)
		self.connect(self.actionStop, QtCore.SIGNAL("triggered(bool)"), self.stop)
		self.connect(self.actionExit, QtCore.SIGNAL("triggered(bool)"), app.quit)
		self.connect(self.searchLine, QtCore.SIGNAL("textEdited(QString)"), self.search)
		self.connect(self.listMusics, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.play)
		self.connect(self.actionColor, QtCore.SIGNAL("triggered(bool)"), self.setColor)
		self.connect(self.actionSettings, QtCore.SIGNAL("triggered(bool)"), self.openConfig)
		self.connect(self.actionAbout, QtCore.SIGNAL("triggered(bool)"), self.about)

		self.db = shelve.open("%s/.kxmp.db" % os.getenv("HOME"))
		self.xmDir = self.db["path"]
		self.db.close()
		
		try:
			if self.xmDir[-1] != "/":
				self.xmDir = self.xmDir + "/"
		except:
			pass
	
		self.db = shelve.open("%s/.kxmp.db" % os.getenv("HOME"))
		self.color = self.db["isColored"]
		self.db.close()

		self.listMusics.setAlternatingRowColors(self.color)
		self.isPlaying = False

		self.cw = configWindow()
		self.connect(self.cw.buttons, QtCore.SIGNAL("accepted()"), self.listXm)

		self.listXm()

	def setColor(self):
		if self.color:
			self.listMusics.setAlternatingRowColors(False)
			color_ = False
		else:
			self.listMusics.setAlternatingRowColors(True)
			color_ = True

		self.color = color_

	def listXm(self):
		self.listMusics.clear()

		self.db = shelve.open("%s/.kxmp.db" % os.getenv("HOME"))
		self.xmDir = self.db["path"]
		self.db.close()

		try:
			if self.xmDir[-1] != "/":
				self.xmDir = self.xmDir + "/"
		except:
			pass

		self.db = shelve.open("%s/.kxmp.db" % os.getenv("HOME"))
		try:
			list_ = os.listdir(self.xmDir)
			if self.db["isShuffle"]:
				shuffle(list_)
				for i in list_:
					self.listMusics.addItem(str(i))
			else:
				for i in list_:
					self.listMusics.addItem(str(i))
		except:
			pass

		self.db.close()

	def play(self):
		try:
		    self.playName = self.xmDir + str(self.listMusics.selectedItems()[0].text())

		    # çalan bir müzik var mı diye denetleniyor...
		    if self.isPlaying:
			    self.stop()
			    self.process = subprocess.Popen(["xmp", "-l", self.playName], stdout=subprocess.PIPE)
			    self.isPlaying = True
			    self.setStatus(_("Playing... ") + unicode(self.playName.split("/")[-1]))

			    tray.showMessage("KXmp Info", _("Playing... ") + self.playName, QtGui.QSystemTrayIcon.Information, 3000)
		    else:
			    self.process = subprocess.Popen(["xmp", "-l", self.playName], stdout=subprocess.PIPE)
			    self.isPlaying = True
			    self.setStatus(_("Playing... ") + unicode(self.playName.split("/")[-1]))

			    tray.showMessage(_("KXmp Info"), _("Playing... ") + self.playName, tray.Information, 3000)
		except IndexError:
		    if not self.isVisible():
			self.show()

		    QtGui.QMessageBox.critical(self, _(u"Music select"), _(u"Music is not selected, please select a music from list..."))

	def search(self):
		self.list = os.listdir(self.xmDir)
		self.listMusics.clear()
		self.db = shelve.open("%s/.kxmp.db" % os.getenv("HOME"))
		for i in self.list:
			if self.db["isIgnoreCase"]:
				if re.search(str(self.searchLine.text()), i):
					self.listMusics.addItem(str(i))
			else:
				if re.search(str(self.searchLine.text()), i, re.IGNORECASE):
					self.listMusics.addItem(str(i))
		self.db.close()

	def stop(self):
		try:
			os.kill(self.process.pid, 15)
			self.isPlaying = False
			self.setStatus(_(u"Stopped..."))
		except:
			pass

	def setStatus(self, message):
	    self.status.setText("<i>%(message)s</i>" % vars())

	def openConfig(self):
		self.cw.show()

	def about(self):
		KAboutApplicationDialog(aboutData, self).show()

aboutData = KAboutData (appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)
aboutData.setProgramIconName(":/icons/icons/sazli.png")
aboutData.addAuthor(ki18n("Oğuzhan Eroğlu"), ki18n(__("Project founder and developer")), "rohanrhu2@gmail.com")
aboutData.addCredit(ki18n("Gökbey Uluç"), ki18n(__("Icons")), "ulucname@gmail.com")

KCmdLineArgs.init(sys.argv, aboutData)
app = KApplication()
app.setQuitOnLastWindowClosed(False)

mw = mainWindow()

pixmap = QtGui.QPixmap(":/icons/metallica.png")
splash = QtGui.QSplashScreen(pixmap)
splash.show()

timer = QtCore.QTimer()

def show(reason):
    if reason == QtGui.QSystemTrayIcon.Trigger:
	if not mw.isVisible():
	    mw.show()
	else:
	    if mw.cw.isVisible():
		mw.cw.done(0)
	    mw.hide()

def showConfig():
	    mw.show()
	    mw.cw.show()

def openWindow():
	splash.hide()
	mw.show()
	timer.stop()

menu = QtGui.QMenu()

exitAction = QtGui.QAction(QtGui.QIcon(u":/top_buttons/icons/exit.png"), _(u"Exit"), None)
settingsAction = QtGui.QAction(QtGui.QIcon(u":/top_buttons/icons/preferences_system.png"), _(u"Settings"), None)
stopAction = QtGui.QAction(QtGui.QIcon(u":/buttons/icons/media_playback_stop.png"), _(u"Stop"), None)
playAction =  QtGui.QAction(QtGui.QIcon(u":/buttons/icons/media_playback_start.png"), _(u"Play"), None)

QtCore.QObject.connect(exitAction, QtCore.SIGNAL("triggered(bool)"), app.exit)
QtCore.QObject.connect(settingsAction, QtCore.SIGNAL("triggered(bool)"), showConfig)
QtCore.QObject.connect(playAction, QtCore.SIGNAL("triggered(bool)"), mw.play)
QtCore.QObject.connect(stopAction, QtCore.SIGNAL("triggered(bool)"), mw.stop)

menu.addAction(playAction)
menu.addAction(stopAction)
menu.addSeparator()
menu.addAction(settingsAction)
menu.addSeparator()
menu.addAction(exitAction)

tray = KSystemTrayIcon(QtGui.QIcon(":/icons/icons/sazli.png"))

QtCore.QObject.connect(tray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), show)

tray.setContextMenu(menu)

tray.show()

QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), openWindow)
timer.start(2000)

import kxmpicons_rc

app.exec_()

if mw.isPlaying:
	os.kill(mw.process.pid, 15)