#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
from PyQt4 import QtGui, QtCore

from menubar import MenuBar

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(800, 600)
        self.setWindowTitle(u"Gestion des budgets ANM")
        #self.setWindowIcon(QtGui.QIcon('icons/anm.png'))

        menubar = MenuBar(self)
        self.setMenuBar(menubar)


