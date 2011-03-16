#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from PyQt4 import QtGui, QtCore

from database import Account
from menubar import MenuBar
from balanceview import BalanceViewWidget
from operationview import OperationWidget


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(900, 650)
        self.setWindowTitle(_(u"ANM Budgets Manager"))
        self.setWindowIcon(QtGui.QIcon('images/icon32.png'))

        self._account = None

        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

        self.change_context(BalanceViewWidget)

    def getaccount(self):
        return self._account

    def setaccount(self, value):
        if not isinstance(value, (Account, None.__class__)):
            raise ValueError(_(u"account must be an Account or None."))
        self._account = value

    def clear_account(self):
        self.account = None

    account = property(getaccount, setaccount)

    def change_context(self, context_widget, *args, **kwargs):
        # remove account before switching
        self.clear_account()

        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # refresh menubar
        self.menubar.refresh()

        # attach context to window
        self.setCentralWidget(self.view_widget)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        d.exec_()
