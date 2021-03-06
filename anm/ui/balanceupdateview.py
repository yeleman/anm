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
from common import ANMWidget, ANMTableWidget, ANMPageTitle


class BalanceUpdateWidget(ANMWidget):

    def __init__(self, parent=0, force_current=False, *args, **kwargs):

        super(BalanceUpdateWidget, self).__init__(parent=parent, \
                                                  *args, **kwargs)
        self.title = ANMPageTitle(_(u"Update Budgets for next Quarter."))

        # periods
        self.period1 = current_period()

        # need to change data for current period since it does not exist.
        if force_current:
            self.period2 = current_period()
            self.title = ANMPageTitle(_(u"You must enter bugets for current period before you can continue."))
        else:
            self.period2 = self.period1.next()
        self.table = NextBalanceUpdateTableWidget(parent=self, \
                                                  period1=self.period1, \
                                                  period2=self.period2)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.table)

        self.setLayout(vbox)

    def refresh(self):
        self.table.refresh()


class NextBalanceUpdateTableWidget(ANMTableWidget):

    def __init__(self, parent, period1, period2, *args, **kwargs):

        ANMTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.period1 = period1
        self.period2 = period2

        try:
            self.data = [account_update_summary(account, \
                                                self.period1, \
                                                self.period2) \
                    for account in session.query(Account).all()]
        except AccountNotConfigured as e:
            raise

        self.header = [_(u"Account N°"), _(u"Account Name"), \
                       _(u"%(period)s budget") \
                         % {'period': self.period1.short_name()}, \
                       _(u"%(period)s budget") \
                         % {'period': self.period2.short_name()}]

        self.setDisplayTotal(True, column_totals={2: None, 3: None}, \
                             label=_(u"TOTALS"))

        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)

        self.refresh(True)

    def extend_rows(self):

        # add a row with SAVE CHANGES button
        nb_rows = self.rowCount()
        self.setRowCount(nb_rows + 1)
        self.setSpan(nb_rows, 0, 1, 3)
        bicon = QtGui.QIcon.fromTheme('document-save', \
                                       QtGui.QIcon('images/document-save.png'))
        self.button = QtGui.QPushButton(bicon, _(u"Commit Changes"))
        self.button.released.connect(self.save_new_data)
        self.setCellWidget(nb_rows, 3, self.button)

    def _item_for_data(self, row, column, data, context=None):
        if column == self.data[0].__len__() - 2:
            line_edit = QtGui.QLineEdit(u"%s" % data)
            line_edit.setValidator(QtGui.QIntValidator())
            line_edit.editingFinished.connect(self.changed_value)
            return line_edit

        return super(NextBalanceUpdateTableWidget, self)\
                                    ._item_for_data(row, column, data, context)

    def changed_value(self, refresh=False):
        # change self.data to reflect new budgets
        for row_num in xrange(0, self.data.__len__()):
            self._update_budget(row_num, \
                                int(self.cellWidget(row_num, 3).text()))
        # we don't refresh table unless asked
        # so that we can forward click events
        if refresh:
            self.refresh()
        # focus on save button
        self.button.setFocus(Qt.MouseFocusReason)

    def _update_budget(self, row_num, budget):
        d = self.data[row_num]
        self.data[row_num] = (d[0], d[1], d[2], budget, d[4])

    def save_new_data(self):
        def actually_save():
            for row in self.data:
                account = row[-1]
                if not isinstance(account, Account):
                    continue

                budget = session.query(Budget).filter_by(account=account, \
                                                         period=self.period2)\
                                              .first()
                budget.amount = row[3]
                session.add(budget)
            session.commit()
        try:
            actually_save()
            self.refresh()
            raise_success(_(u"Budgets Updated!"), \
                          _(u"The budgets for %(period)s have been " \
                            u"successfully updated.") \
                            % {'period': self.period2.short_name()})
        except Exception as e:
            raise_success(_(u"Error updating budgets!"), \
                          _(u"There has been an error while trying to " \
                            u"save the new budgets:\n%(error)s") \
                            % {'error': e})
