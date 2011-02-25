#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad


import re
import operator

from database import *
from sqlalchemy import desc
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QVariant, Qt


class UpdateBalancesWidget(QtGui.QWidget):

    def __init__(self):

        QtGui.QWidget.__init__(self)
        #~ account = QLineEdit()

        self.data = [(bud.account.number, bud.account.name, bud.amount)\
                            for bud in session.query(Budget).all()]

        print self.data

        # create the view
        table = QtGui.QTableView()
        # set the table model
        header = [_(u"Number Compte"), _(u"name Compte"), _(u"Previous Amount"),
                  _(u'Next amount')]
        tm = MyTableModel(self.data, header, self)
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
        nrows = len(self.data)
        for row in xrange(nrows):
            table.setRowHeight(row, 20)

        # selects the line
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(QtGui.QLabel(u"Balance update"))

        hbox3 = QtGui.QFormLayout()
        #~ startdateLineEdit = QtGui.QLineEdit()
        #~ enddateLineEdit = QtGui.QLineEdit()
        #~ hbox3.addRow(u"start date", startdateLineEdit)
        #~ hbox3.addRow(u"end date", enddateLineEdit)
        hbox3.addWidget(QtGui.QPushButton("OK"))

        tablebox = QtGui.QHBoxLayout()
        tablebox.addWidget(table)

        QtGui.QVBoxLayout()

        vbox = QtGui.QVBoxLayout()

        vbox.addLayout(hbox3)
        vbox.addLayout(hbox2)
        vbox.addLayout(tablebox)

        self.setLayout(vbox)

class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):

        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0]) + 1

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
