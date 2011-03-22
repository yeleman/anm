#!/usr/bin/env python
# encoding=utf-8
# maintainer: Alou

from PyQt4 import QtGui
from PyQt4 import QtCore

from sqlalchemy import desc

from common import ANMWidget
from database import Period, session, Account
from data_helpers import current_period, all_active_periods
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
        self.all_active_periods = all_active_periods(session.query(Period).\
                           order_by(desc(Period.start_on)).all())

        self.data_account = session.query(Account).all()

        self.box_account.addItem(_(u"All Accounts"))
        for index in xrange(0, len(self.data_account)):
            account = self.data_account[index]
            self.box_account.addItem(_(u'%(number)s %(name)s') %\
                        {'number': account.number, 'name': account.name})

        sel_index = 0
        for index in xrange(0, len(self.all_active_periods)):
            ped = self.all_active_periods[index]
            if ped == current_period():
                sel_index = index
            self.box_period.addItem(_(u'%(display_name)s') %\
                                {'display_name': ped.display_name()})
        self.box_period.setCurrentIndex(sel_index)

        #Ok and cancel hbox
        button_hbox = QtGui.QHBoxLayout()

        #Ok Button widget.
        operation_but = QtGui.QPushButton(_("list of operations per account"))
        button_hbox.addWidget(operation_but)
        operation_but.clicked.connect(self.Operation_pdf)

        #Cancel Button widget.
        balance_but = QtGui.QPushButton(_("Balances (All accounts)"))
        button_hbox.addWidget(balance_but)
        balance_but.clicked.connect(self.balance_pdf)

        combo_hbox = QtGui.QHBoxLayout()
        combo_hbox.addWidget(self.box_account)
        combo_hbox.addWidget(self.box_period)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(combo_hbox)
        vbox.addLayout(button_hbox)
        self.setLayout(vbox)

    def balance_pdf(self):
        period = self.all_active_periods[self.box_period.currentIndex()]
        pdf_report = build_accounts_report(period=period)
        uopen_file(pdf_report)

    def Operation_pdf(self):
        """ """
        index = self.box_account.currentIndex()
        if index > 0:
            account = self.data_account[index - 1]
        else:
            account = None
        period = self.all_active_periods[self.box_period.currentIndex()]
        pdf_report = build_operations_report(account=account, \
                                period=period)
        uopen_file(pdf_report)
