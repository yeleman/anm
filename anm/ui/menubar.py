#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
from PyQt4 import QtGui, QtCore

from balanceview import BalanceViewWidget


class MenuBar(QtGui.QMenuBar):

    def __init__(self, parent=None):
        QtGui.QMenuBar.__init__(self, parent)
        #menubar = self.menuBar()

        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        self.connect(exit, QtCore.SIGNAL('triggered()'), \
                                         self.parentWidget(), \
                                         QtCore.SLOT('close()'))

        file_ = self.addMenu('&File')
        file_.addAction(exit)

        # accounts
        balance = QtGui.QAction('View all balances', self)
        balance.setShortcut('Ctrl+H')
        self.connect(balance, QtCore.SIGNAL('triggered()'), self.goto_balance)

        blank = QtGui.QAction('TEST BLANK', self)
        self.connect(blank, QtCore.SIGNAL('triggered()'), self.goto_blank)

        accounts = self.addMenu('&Accounts')
        accounts.addAction(balance)
        accounts.addAction(blank)

    def goto_balance(self):
        self.parentWidget().switch_context(BalanceViewWidget())

    def goto_blank(self):
        self.parentWidget().switch_context(QtGui.QWidget())
