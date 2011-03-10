#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad


import re
import operator

from sqlalchemy import desc
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QVariant, Qt

from database import Budget, session, Account
from data_helpers import current_period, AccountNotConfigured, \
                         account_summary, account_update_summary
from utils import raise_error, raise_success
from common import ANMWidget, ANMTableWidget


class BalanceUpdateWidget(ANMWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent=parent, *args, **kwargs)

        self.table = NextBalanceUpdateTableWidget(parent=self)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.table)

        # periods
        period = current_period()

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()


class NextBalanceUpdateTableWidget(ANMTableWidget):

    def __init__(self, parent, *args, **kwargs):

        ANMTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.period = current_period()
        try:
            self.data = [account_update_summary(account, \
                                                self.period, \
                                                self.period.next()) \
                    for account in session.query(Account).all()]
        except AccountNotConfigured as e:
            raise

        self.header = [_(u"Account number"), _(u"Account Name"), \
                       _(u"%(period)s budget") \
                         % {'period': self.period.short_name()}, \
                       _(u"%(period)s budget") \
                         % {'period': self.period.next().short_name()}]

        self.setDisplayTotal(True, column_totals={2: None, 3: None}, \
                             label=_(u"TOTALS"))

        self.refresh()

    def refresh(self):
        if not self.data or not self.header:
            return

        # increase rowCount by one if we have to display total row
        rc = self.data.__len__()
        if self._display_total:
            rc += 1
        self.setRowCount(rc)
        self.setColumnCount(self.header.__len__())
        self.setHorizontalHeaderLabels(self.header)

        n = 0
        for row in self.data:
            m = 0
            for item in row:
                if m == row.__len__() - 2:
                    line_edit = QtGui.QLineEdit(u"%s" % item)
                    line_edit.setValidator(QtGui.QIntValidator())
                    line_edit.editingFinished.connect(self.changed_value)
                    #newitem = QtGui.QTableWidgetItem(\
                    #                QtGui.QIcon("images/go-next.png"), '')
                    self.setCellWidget(n, m, line_edit)
                else:
                    newitem = QtGui.QTableWidgetItem(\
                                                  self._format_for_table(item))
                    self.setItem(n, m, newitem)
                m += 1
            n += 1

        self._display_total_row()

        self.resizeColumnsToContents()

    def changed_value(self):
        # change self.data to reflect new budgets
        for row_num in xrange(0, self.data.__len__()):
            self._update_budget(row_num, \
                                int(self.cellWidget(row_num, 3).text()))
        # refresh table
        self.refresh()

    def _update_budget(self, row_num, budget):
        d = self.data[row_num]
        self.data[row_num] = (d[0], d[1], d[2], budget, d[4])
