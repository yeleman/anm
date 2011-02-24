#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from PyQt4 import QtGui, QtCore

from menubar import MenuBar
from balanceview import BalanceViewWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(800, 600)
        self.setWindowTitle(_(u"ANM Budgets Manager"))
        #self.setWindowIcon(QtGui.QIcon('icons/anm.png'))

        menubar = MenuBar(self)
        self.setMenuBar(menubar)

        self.switch_context(BalanceViewWidget())

    def switch_context(self, context_widget):
        self.view_widget = context_widget
        self.setCentralWidget(self.view_widget)
