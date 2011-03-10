#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from database import Account, session, Period
from data_helpers import current_period, AccountNotConfigured, account_summary
from common import ANMWidget, ANMTableWidget
from operationview import OperationWidget


class BalanceViewWidget(ANMWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent=parent, *args, **kwargs)

        self.table = BalanceTableWidget(parent=self)
        self.table.setMaximumWidth(900)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.table)

        # periods
        period = current_period()
        self.tabbar = QtGui.QTabBar()
        self.tabbar.addTab(period.previous().display_name())
        self.tabbar.addTab(period.display_name())
        self.tabbar.addTab(period.next().display_name())
        self.tabbar.setCurrentIndex(1)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tabbar)
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

        self.header = [_(u"Account No."), _(u"Name"), \
                        _(u"Budget"), _(u"Balance"), \
                        _(u"Go")]

        self.setDisplayTotal(True, column_totals={2: None, 3: None}, \
                             label=_(u"TOTALS"))

        self.refresh()

    def resizeEvent(self, event):
        self.move(self.left_pos, self.y())

    def _item_for_data(self, row, column, data, context=None):
        if column == self.data[0].__len__() - 1:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/go-next.png"), \
                                          '')
        return super(BalanceTableWidget, self)\
                                    ._item_for_data(row, column, data, context)

    def click_item(self, row, column, *args):
        last_column = self.header.__len__() - 1
        if column != last_column:
            return

        self.parent.change_main_context(OperationWidget, \
                                        account=self.data[row][last_column])
