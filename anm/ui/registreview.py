#!/usr/bin/env python
# encoding=utf-8
# maintainer: Alou

from PyQt4 import QtGui
from PyQt4 import QtCore

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
        title.setText(_(u"Choose a period and a type"))
        title.setAlignment(QtCore.Qt.AlignHCenter)
        title_hbox = QtGui.QHBoxLayout()
        title_hbox.addWidget(title)

        #Combobox widget
        self.box_account = QtGui.QComboBox()
        self.box_period = QtGui.QComboBox()
        self.box_type = QtGui.QComboBox()

        # Data
        current = current_period()
        self.data_period = session.query(Period).all()
        self.data_account = session.query(Account).all()
        self.data_type = ['balance', 'operation']

        self.box_account.addItem(_(u"All Accounts"))
        for index in xrange(0, len(self.data_account)):
            account = self.data_account[index]
            self.box_account.addItem(u'%s' % account.name)

        for index in xrange(0, len(self.data_period)):
            ped = self.data_period[index]
            self.box_period.addItem(u'%s' % (ped.name))

        for index in xrange(0, len(self.data_type)):
            pe = self.data_type[index]
            self.box_type.addItem(u'%s' % (pe))

        #Ok and cancel hbox
        button_hbox = QtGui.QHBoxLayout()

        #Ok Button widget.
        ok_but = QtGui.QPushButton(_("OK"))
        button_hbox.addWidget(ok_but)
        ok_but.clicked.connect(self.capture_ok)

        #Cancel Button widget.
        cancel_but = QtGui.QPushButton(_("Cancel"))
        button_hbox.addWidget(cancel_but)
        cancel_but.clicked.connect(self.cancel)

        combo_hbox = QtGui.QHBoxLayout()
        combo_hbox1 = QtGui.QHBoxLayout()
        combo_hbox.addWidget(self.box_account)
        combo_hbox.addWidget(self.box_period)
        combo_hbox.addWidget(self.box_type)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(combo_hbox)
        vbox.addLayout(button_hbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def capture_ok(self):
        index = self.box_account.currentIndex()
        if index > 0:
            account = self.data_account[index - 1]
        else:
            account = None
        period = self.data_period[self.box_period.currentIndex()]
        type = self.data_type[self.box_type.currentIndex()]

        if type == 'balance':
            pdf_report = build_accounts_report(period=period, \
                                               filename=u'balance.pdf')
        elif type == 'operation':
            pdf_report = build_operations_report(account=account, \
                                        period=period, filename=u'operation.pdf')
        uopen_file(pdf_report)
