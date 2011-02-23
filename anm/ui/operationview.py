#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

import re
import operator
from database import *
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QVariant, Qt

class OperationViewWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        # add data
        self.data = [(op.order_number, op.invoice_number, \
                      op.invoice_date.strftime('%F'), op.provider, op.amount) \
                      for op in session.query(Operation).all()]

        tv = QtGui.QTableView()

        # set the table model
        header = ['Number mandat', 'Numero facture', 'date facture',
                  'fournisseur', 'Montant TTC']
        tm = MyTableModel(self.data, header, self)
        tv.setModel(tm)
        tv.setSortingEnabled(True)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(tv)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):

        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

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
