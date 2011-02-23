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

        print_ = QtGui.QAction('Print', self)
        print_.setShortcut('Ctrl+P')
        self.connect(print_, QtCore.SIGNAL('triggered()'), self.goto_print)

        file_ = self.addMenu('&File')
        file_.addAction('Delete operation', self.goto_delete_operation)
        file_.addAction(print_)
        file_.addAction('Export data', self.goto_export_data)
        file_.addAction(exit)

        #aller à
        goto = QtGui.QAction('Go to', self)
        file_ = self.addMenu('&Go to')
        file_.addAction('List of balance', self.goto_list_of_balances)
        file_.addAction('The updated budget', self.goto_updated_budget)
        #Aide
        file_ = self.addMenu('Help')
        file_.addAction('About', self.goto_about)

    #balance
    def goto_balance(self):
        print 'balance'

    #Print
    def goto_print(self):
        print 'Processing a Print Request'

    def goto_delete_operation(self):
        print 'deleted'

    def goto_export_data(self):
        print 'export data'

    #list_of_balances
    def goto_list_of_balances(self):
        self.parentWidget().switch_context(BalanceViewWidget())

    #mise à jour de budget
    def goto_updated_budget(self):
        print 'updated budget'

    #About
    def goto_about(self):
        print 'About'
