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
import os
import sys
import locale
import gettext

local, encoding = locale.getdefaultlocale()

_ = gettext.translation("kxmp", fallback=True, languages=[local]).ugettext

class Ui_configWindow(object):
    def setupUi(self, configWindow):
        configWindow.setObjectName("configWindow")
        configWindow.resize(382, 285)
        configWindow.setMaximumSize(QtCore.QSize(400, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/sazli.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        configWindow.setWindowIcon(icon)
        self.tabWidget = QtGui.QTabWidget(configWindow)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 361, 231))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 18))
        self.label.setObjectName("label")
        self.line = QtGui.QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(10, 70, 331, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.isIgnoreCase = QtGui.QCheckBox(self.tab)
        self.isIgnoreCase.setGeometry(QtCore.QRect(10, 100, 251, 23))
        self.isIgnoreCase.setChecked(False)
        self.isIgnoreCase.setObjectName("isIgnoreCase")
        self.pathLine = QtGui.QLineEdit(self.tab)
        self.pathLine.setGeometry(QtCore.QRect(10, 30, 311, 29))
        self.pathLine.setObjectName("pathLine")
        self.dirSelectButton = QtGui.QToolButton(self.tab)
        self.dirSelectButton.setGeometry(QtCore.QRect(320, 30, 30, 28))
        self.dirSelectButton.setObjectName("dirSelectButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.isShuffle = QtGui.QCheckBox(self.tab_2)
        self.isShuffle.setGeometry(QtCore.QRect(20, 30, 281, 23))
        self.isShuffle.setObjectName("isShuffle")
        self.isColored = QtGui.QCheckBox(self.tab_2)
        self.isColored.setGeometry(QtCore.QRect(20, 70, 151, 23))
        self.isColored.setObjectName("isColored")
        self.tabWidget.addTab(self.tab_2, "")
        self.buttons = QtGui.QDialogButtonBox(configWindow)
        self.buttons.setGeometry(QtCore.QRect(8, 250, 361, 28))
        self.buttons.setAutoFillBackground(False)
        self.buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttons.setCenterButtons(False)
        self.buttons.setObjectName("buttons")

        self.retranslateUi(configWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(configWindow)

    def retranslateUi(self, configWindow):
        configWindow.setWindowTitle(_("KXmp Settings"))
        self.label.setText(_("Musics path:"))
        self.dirSelectButton.setText(_("..."))
        self.isIgnoreCase.setText(_("Case sensitivity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _("General"))
        self.isShuffle.setText(_("Mixed listing"))
        self.isColored.setText(_("List colors"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _("Advanced"))

import kxmpicons_rc
