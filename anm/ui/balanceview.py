#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from database import *
from data_helpers import *
from operationview import OperationWidget


class BalanceViewWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        table = BalanceTableWidget(parent=self)
        table.setSortingEnabled(True)
        table.setShowGrid(True)
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        table.setCornerButtonEnabled(True)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(table)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)


class BalanceTableWidget(QtGui.QTableWidget):

    def __init__(self, parent, *args):

        self.parent = parent
        self.period = session.query(Period).first()
        try:
            self.data = [account_summary(account, self.period)
                        for account in session.query(Account).all()]
        except AccountNotConfigured as e:
            pass

        self.headers = [_(u'Account number'), _(u'Account Name'), \
                        _(u'Account budget'), _(u'Account balance'), \
                        _(u'Go To')]

        QtGui.QTableWidget.__init__(self, *args)
        self.setColumnCount(self.headers.__len__())
        self.setRowCount(15)

        self.setHorizontalHeaderLabels(self.headers)

        self.setmydata()

        self.cellClicked.connect(self.click_item)

    def setmydata(self):
        n = 0
        for row in self.data:
            m = 0
            skip = True
            for item in row:
                if m == row.__len__() - 1:
                    newitem = QtGui.QTableWidgetItem(\
                                    QtGui.QIcon('images/go-next.png'), \
                                    _(u"View detail"))
                else:
                    newitem = QtGui.QTableWidgetItem(u'%s' % item)
                self.setItem(n, m, newitem)
                m += 1
            n += 1

    def click_item(self, row, column, *args):
        last_column = self.headers.__len__() - 1
        if column != last_column:
            return

        self.parent.parentWidget().switch_context(\
                          OperationWidget(account=self.data[row][last_column]))
