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
        table = QtGui.QTableView()

        # set the table model
        header = [_(u'Order number'), _(u'Invoice number'), _(u'Invoice date'),
                  _(u'Provider'), _(u'Amount')]
        tm = MyTableModel(self.tabledata, header, self)
        table.setModel(tm)

        # active sorting
        table.setSortingEnabled(True)

        table.sortByColumn(2, Qt.DescendingOrder)

        # set the font
        font = QtGui.QFont("Courier New", 10)
        table.setFont(font)

        # hide vertical header
        vh = table.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = table.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        table.resizeColumnsToContents()

        # set row height
        nrows = len(self.tabledata)
        for row in xrange(nrows):
            table.setRowHeight(row, 20)

        # selects the line
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        table.clicked.connect(self.goto_operations)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(table)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(QtGui.QLabel("Account transactions %s (%s)" %\
                                     (self.account.name, self.account.number)))
        hbox2.setAlignment(Qt.AlignHCenter)
        hbox3 = QtGui.QFormLayout()
        self.order_number = QtGui.QLineEdit()
        self.invoice_number = QtGui.QLineEdit()
        self.invoice_date = QtGui.QLineEdit()
        self.provider = QtGui.QLineEdit()
        self.amount = QtGui.QLineEdit()
        butt = QtGui.QPushButton(_(u"Add"))
        hbox3.addRow(_(u'Order number'), self.order_number)
        hbox3.addRow(_(u'Invoice number'), self.invoice_number)
        hbox3.addRow(_(u'Invoice date'), self.invoice_date)
        hbox3.addRow(_(u'Provider'), self.provider)
        hbox3.addRow(_(u'Amount'), self.amount)
        hbox3.addWidget(butt)

        self.connect(butt, QtCore.SIGNAL('clicked()'), self.goto)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def goto(self):
        print self.invoice_date.text()
        achat = Operation(self.order_number.text(), self.invoice_number.text(), datetime.today(), \
                  self.provider.text(), self.amount.text())
        achat.account = self.account

        session.add(achat)
        session.commit()
        #~ account = session.query(Account).filter_by(number=account_id).one()
        #~ self.parentWidget().switch_context(OperationWidget(account=account))

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
        return len(self.arraydata[0]) - 1

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

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))
