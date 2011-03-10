#!/usr/bin/env python
# encoding=utf-8
# maintainer: Alou

from PyQt4 import QtGui
from PyQt4 import QtCore

from sqlalchemy import desc

from common import ANMWidget
from database import Period, session, Account
from data_helpers import current_period
from prints import build_accounts_report, build_operations_report
from utils import uopen_file


class RegistreWidget(QtGui.QDialog, ANMWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent, *args, **kwargs)

        self.setWindowTitle(_(u"Choice of type and period"))

        #Title widget
        title = QtGui.QLabel()
        title.setText(_(u"Choose a account and a period"))
        title.setAlignment(QtCore.Qt.AlignHCenter)
        title_hbox = QtGui.QHBoxLayout()
        title_hbox.addWidget(title)

        #Combobox widget
        self.box_account = QtGui.QComboBox()
        self.box_period = QtGui.QComboBox()
        self.box_type = QtGui.QComboBox()

        # Data
        current = current_period()
        self.data_period = session.query(Period).\
                           order_by(desc(Period.start_on)).all()
        self.data_account = session.query(Account).all()

        self.box_account.addItem(_(u"All Accounts"))
        for index in xrange(0, len(self.data_account)):
            account = self.data_account[index]
            self.box_account.addItem(_(u'%(number)s %(name)s') %\
                        {'number': account.number, 'name': account.name})

        for index in xrange(0, len(self.data_period)):
            ped = self.data_period[index]
            self.box_period.addItem(_(u'%(display_name)s') %\
                                {'display_name': ped.display_name()})

        #Ok and cancel hbox
        button_hbox = QtGui.QHBoxLayout()

        #Ok Button widget.
        operation_but = QtGui.QPushButton(_("Operation"))
        button_hbox.addWidget(operation_but)
        operation_but.clicked.connect(self.Operation_pdf)

        #Cancel Button widget.
        balance_but = QtGui.QPushButton(_("Balance"))
        button_hbox.addWidget(balance_but)
        balance_but.clicked.connect(self.balance_pdf)

        combo_hbox = QtGui.QHBoxLayout()
        combo_hbox1 = QtGui.QHBoxLayout()
        combo_hbox.addWidget(self.box_account)
        combo_hbox.addWidget(self.box_period)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(combo_hbox)
        vbox.addLayout(button_hbox)
        self.setLayout(vbox)

    def balance_pdf(self):
        period = self.data_period[self.box_period.currentIndex()]
        pdf_report = build_accounts_report(period=period, \
                                               filename=_(u'balance.pdf'))
        uopen_file(pdf_report)

    def Operation_pdf(self):
        index = self.box_account.currentIndex()
        if index > 0:
            account = self.data_account[index - 1]
        else:
            account = None
        period = self.data_period[self.box_period.currentIndex()]

        pdf_report = build_operations_report(account=account, \
                                    period=period, filename=_(u'operation.pdf'))
        uopen_file(pdf_report)
