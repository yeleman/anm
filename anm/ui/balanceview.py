#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from database import Account, session, Period
from data_helpers import current_period, AccountNotConfigured, account_summary
from common import ANMWidget, ANMTableWidget, ANMPeriodHolder, ANMPageTitle
from operationview import OperationWidget


class BalanceViewWidget(ANMWidget, ANMPeriodHolder):

    def __init__(self, parent=0, *args, **kwargs):

        super(BalanceViewWidget, self).__init__(parent=parent, *args, **kwargs)
        ANMPeriodHolder.__init__(self, *args, **kwargs)

        self.title = ANMPageTitle(_(u"Account's Summary."))

        self.table = BalanceTableWidget(parent=self, period=self.main_period)

        # periods
        period = current_period()

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.periods_bar)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()

    def change_period(self, period):
        self.table.refresh_period(period)


class BalanceTableWidget(ANMTableWidget):

    def __init__(self, parent, period, *args, **kwargs):

        ANMTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.header = [_(u"Account No."), _(u"Name"), \
                        _(u"Budget"), _(u"Balance"), \
                        _(u"Go")]

        self.setDisplayTotal(True, column_totals={2: None, 3: None}, \
                             label=_(u"TOTALS"))

        self.set_data_for(period)

        self.refresh(True)

    def refresh_period(self, period):
        self.main_period = period
        self.set_data_for(period)
        self.refresh()

    def set_data_for(self, period=current_period()):
        self.data = [account_summary(account, period)
                for account in session.query(Account).all()]

    def _item_for_data(self, row, column, data, context=None):
        if column == self.data[0].__len__() - 1:
            return QtGui.QTableWidgetItem(QtGui.QIcon("images/go-next.png"), \
                                          _(u"Operations"))
        return super(BalanceTableWidget, self)\
                                    ._item_for_data(row, column, data, context)

    def click_item(self, row, column, *args):
        last_column = self.header.__len__() - 1
        if column != last_column:
            return

        self.parent.change_main_context(OperationWidget, \
                                        account=self.data[row][last_column], \
                                        period=self.parentWidget().main_period)
