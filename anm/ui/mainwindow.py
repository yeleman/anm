#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from PyQt4 import QtGui, QtCore

from menubar import MenuBar
from balanceview import BalanceViewWidget
from operationview import OperationWidget


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(800, 600)
        self.setWindowTitle(_(u"ANM Budgets Manager"))
        #self.setWindowIcon(QtGui.QIcon('icons/anm.png'))

        self.clear_account()

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

        self.switch_context(BalanceViewWidget())

    def switch_context(self, context_widget):
        if context_widget.__class__ != OperationWidget:
            self.clear_account()
        self.menubar.refresh()
        self.view_widget = context_widget
        self.setCentralWidget(self.view_widget)
    
    def clear_account(self):
        self.account = None
    
    def set_account(self, account):
        self.account = account
