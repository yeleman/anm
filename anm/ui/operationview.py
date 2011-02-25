#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

import re
import operator
from datetime import datetime
from database import Operation, session
from sqlalchemy import desc
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QVariant, Qt, QObject


class OperationWidget(QtGui.QWidget):

    def __init__(self, account):
        QtGui.QWidget.__init__(self)

        self.account = account

        # add data
        self.tabledata = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime('%F'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      filter_by(account=self.account).\
                      order_by(desc(Operation.invoice_date)).all()]

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

        self.table.clicked.connect(self.goto_operations)

        tablebox = QtGui.QHBoxLayout()
        title = QtGui.QHBoxLayout()

        title.addWidget(QtGui.QLabel("Account transactions %s (%s)" %\
                                     (self.account.name, self.account.number)))
        tablebox.addWidget(self.table)

        formbox = QtGui.QFormLayout()
        self.order_number = QtGui.QLineEdit()
        self.invoice_number = QtGui.QLineEdit()
        self.invoice_date = QtGui.QLineEdit()
        self.provider = QtGui.QLineEdit()
        self.amount = QtGui.QLineEdit()
        butt = QtGui.QPushButton(_(u"Add"))

        formbox1 = QtGui.QHBoxLayout()
        formbox1.addWidget(QtGui.QLabel('order_number'))
        formbox1.addWidget(QtGui.QLabel('invoice_number'))
        formbox1.addWidget(QtGui.QLabel('invoice_date'))
        formbox1.addWidget(QtGui.QLabel('provider'))
        formbox1.addWidget(QtGui.QLabel('amount'))

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

        self.setLayout(vbox)

    def add_operation(self):
        operation = Operation(str(self.order_number.text()),
                    str(self.invoice_number.text()), datetime.today(), \
                    str(self.provider.text()), str(self.amount.text()))
        operation.account = self.account

        session.add(operation)
        session.commit()
        last_operation = session.query(Operation).all()[-1]

        self.parentWidget().switch_context(OperationWidget(self.account))

    def goto_operations(self, index):
        op = self.tabledata[index.row()][self.tabledata[0].__len__() - 1]
        QtGui.QMessageBox.information(self, "OPP", 'operation: %s %s' \
                % (op.invoice_number, op.invoice_date.strftime('%F')))


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

