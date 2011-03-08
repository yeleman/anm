#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from database import *
from data_helpers import *
from common import ANMWidget, ANMTableWidget
from operationview import OperationWidget


class BalanceViewWidget(ANMWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent=parent, *args, **kwargs)

        self.table = BalanceTableWidget(parent=self)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.table)

        # periods
        period = current_period()
        tabbar = QtGui.QTabBar()
        tabbar.addTab(period.previous().display_name())
        tabbar.addTab(period.display_name())
        tabbar.addTab(period.next().display_name())
        tabbar.setCurrentIndex(1)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(tabbar)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()


class BalanceTableWidget(ANMTableWidget):

    def __init__(self, parent, *args, **kwargs):

        ANMTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.period = session.query(Period).first()
        try:
            self.data = [account_summary(account, self.period)
                    for account in session.query(Account).all()]
        except AccountNotConfigured as e:
            raise

        self.header = [_(u"Account number"), _(u"Account Name"), \
                        _(u"Account budget"), _(u"Account balance"), \
                        _(u"Go")]

        self.setDisplayTotal(True, column_totals={2: None, 3: None}, \
                             label=_(u"TOTALS"))

        self.refresh()

    def click_item(self, row, column, *args):
        last_column = self.header.__len__() - 1
        if column != last_column:
            return

        self.parent.change_main_context(OperationWidget, \
                                        account=self.data[row][last_column])
