#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

import re
import operator

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QVariant, Qt, QObject

from sqlalchemy import func, desc

from datetime import date

from common import ANMWidget
from database import Operation, session
from utils import raise_success, raise_error
from deleteview import deleteViewWidget
from data_helpers import *

class OperationWidget(ANMWidget):

    def __init__(self, account, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent, *args, **kwargs)

        # set global account
        self.account = account

        # add data
        self.tabledata = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime('%F'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      filter_by(account=self.account).\
                      order_by(desc(Operation.invoice_date)).all()]

        # calcul total
        self.total = session.query(func.sum(Operation.amount))\
                   .filter_by(account=self.account).scalar()
        if self.total == None:
            self.total = 0

        # create the view
        self.table = QtGui.QTableView()

        # set the table model
        header = [_(u'Order number'), _(u'Invoice number'), _(u'Invoice date'),
                  _(u'Provider'), _(u'Amount')]
        tm = MyTableModel(self.tabledata, header, self)
        self.table.setModel(tm)

        # set the font
        font = QtGui.QFont("Courier New", 10)
        self.table.setFont(font)

        # hide vertical header
        vh = self.table.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = self.table.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.table.resizeColumnsToContents()

        # set row height
        nrows = len(self.tabledata)
        for row in xrange(nrows):
            self.table.setRowHeight(row, 20)

        # selects the line
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        tablebox = QtGui.QHBoxLayout()
        title = QtGui.QHBoxLayout()

        title.addWidget(QtGui.QLabel(_("Account transactions %s (%s)") %\
                                     (self.account.name, self.account.number)))
        tablebox.addWidget(self.table)

        formbox = QtGui.QFormLayout()
        self.order_number = QtGui.QLineEdit()
        self.invoice_number = QtGui.QLineEdit()
        self.invoice_date = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())
        self.invoice_date.setDisplayFormat("yyyy-MM-dd")
        self.provider = QtGui.QLineEdit()
        self.amount = QtGui.QLineEdit()
        self.amount.setValidator(QtGui.QIntValidator())
        butt = QtGui.QPushButton(_(u"Add"))
        totalbox = QtGui.QHBoxLayout()
        totalbox.addWidget(QtGui.QLabel(_(u'Total')))
        totalbox.addWidget(QtGui.QLabel(str(self.total)))

        formbox1 = QtGui.QHBoxLayout()
        formbox1.addWidget(QtGui.QLabel(_(u'Order number')))
        formbox1.addWidget(QtGui.QLabel(_(u'Invoice number')))
        formbox1.addWidget(QtGui.QLabel(_(u'Invoice date')))
        formbox1.addWidget(QtGui.QLabel(_(u'Provider')))
        formbox1.addWidget(QtGui.QLabel(_(u'Amount')))

        formbox = QtGui.QHBoxLayout()
        formbox.addWidget(self.order_number)
        formbox.addWidget(self.invoice_number)
        formbox.addWidget(self.invoice_date)
        formbox.addWidget(self.provider)
        formbox.addWidget(self.amount)
        formbox.addWidget(butt)

        self.connect(butt, QtCore.SIGNAL('clicked()'), self.add_operation)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title)
        vbox.addLayout(formbox1)
        vbox.addLayout(formbox)
        vbox.addLayout(tablebox)
        vbox.addLayout(totalbox)

        self.setLayout(vbox)

    def add_operation(self):
        """add operation"""
        year, month, day = self.invoice_date.text().split('-')
        invoice_date = date(int(year), int(month), int(day))
        period = period_for(invoice_date)
        current_peri = current_period()
        balance = account_balance(self.account, current_peri)
        try:
            amount = int(self.amount.text())
        except ValueError:
            amount = 0
        if self.order_number.text() and self.invoice_number.text() and \
            invoice_date and self.provider.text()and self.amount.text()\
            and invoice_date > current_peri.start_on and invoice_date < \
            current_peri.end_on and amount < balance:
            operation = Operation(unicode(self.order_number.text()),
                        unicode(self.invoice_number.text()), invoice_date, \
                        unicode(self.provider.text()), amount)
            operation.account = self.account
            operation.period = period
            session.add(operation)
            session.commit()

            self.refresh()
            raise_success(_(u'Confirmation'), _(u'Registered opération'))

        elif invoice_date > current_peri.end_on or\
             invoice_date < current_peri.start_on:
            raise_error(_(u'Error date'), \
            _(u'The date is not included in the current quarter.'))
        elif amount > balance:
            raise_error(_(u'Error money'),\
             _(u"There is not enough money for this operation."))
        else:
            raise_error(_(u'Error field'), _(u'You must fill in all fields.'))

    def refresh(self):
        self.change_main_context(OperationWidget, account=self.account)


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):

        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        try:
            return len(self.arraydata[0]) - 1
        except IndexError:
            return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()
