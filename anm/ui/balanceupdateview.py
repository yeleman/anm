#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad


import re
import operator

from sqlalchemy import desc
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QVariant, Qt

from database import *
from data_helpers import *
from utils import raise_error, raise_success
from common import ANMWidget


class UpdateBalancesWidget(ANMWidget):

    def __init__(self, parent, *args, **kwargs):

        QtGui.QWidget.__init__(self, *args, **kwargs)

        self.data = [(bud.account.number, bud.account.name, 0)\
                            for bud in session.query(Budget).all()]

        # create the view
        self.table = QtGui.QTableView()
        # set the table model
        header = [_(u"Account numbers"), _(u"Account names"),\
                                        _(u'New amount')]
        tm = MyTableModel(self.data, header, self)
        self.table.setModel(tm)

        # set the font
        font = QtGui.QFont("Courier New", 10)
        self.table.setFont(font)

        # hide vertical header
        vh = self.table.verticalHeader()

        # set horizontal header properties
        hh = self.table.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.table.resizeColumnsToContents()

        # set row height
        nrows = len(self.data)
        for row in xrange(nrows):
            self.table.setRowHeight(row, 20)

        # selects the line
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        titlebox = QtGui.QHBoxLayout()
        titlebox.addWidget(QtGui.QLabel(_(u"Update periodic budgets")))

        buttonbox = QtGui.QHBoxLayout()

        button = QtGui.QPushButton(_("Save"))
        buttonbox.addWidget(QtGui.QLabel(""))
        buttonbox.addWidget(QtGui.QLabel(""))
        buttonbox.addWidget(button)

        self.connect(button, QtCore.SIGNAL('clicked()'), self.saveupdate)
        tablebox = QtGui.QHBoxLayout()
        tablebox.addWidget(self.table)

        QtGui.QVBoxLayout()

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(titlebox)
        vbox.addLayout(tablebox)
        vbox.addLayout(buttonbox)
        self.setLayout(vbox)

    def saveupdate(self):
        ''' To save the new budget in the database '''

        # on récupère la période en fonction de la date d'aujourd'hui
        try:
            period_ = current_period()
        except:
            title_ = _(u"Adding operation budget")
            message_ = _(u"was already recorded ")
            raise_error(title_, message_)

        flag = True
        for row in self.data:
            number, account_name, new_amount = row[0], row[1], row[2]
            account_ = Account(number, account_name)
            budget = Budget(new_amount)
            budget.period = period_
            budget.account = account_
            session.add_all((period_, account_, budget))
            #save
            try:
                session.commit()
            except:
                session.rollback()
                flag = False

        title_ = _(u"Adding operation budget")
        if flag == True:
            message_ = _(\
            u"The budget for the period %s has been well recorded ")\
             % period_
            raise_success(title_, message_)
        if flag == False:
            message_ = _(\
            u"The budget for the period %s it does not properly recorded ")\
             % period_
            raise_error(title_, message_)


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
