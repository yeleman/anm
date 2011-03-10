#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from PyQt4 import QtGui
from PyQt4 import QtCore

from sqlalchemy import desc

from datetime import date

from common import ANMWidget, ANMTableWidget
from database import Operation, session, Period
from utils import raise_success, raise_error
from data_helpers import account_balance, period_for, current_period


class OperationWidget(ANMWidget):
    def __init__(self, account, parent=0, *args, **kwargs):
        super(OperationWidget, self).__init__(parent=parent, *args, **kwargs)

        # set global account
        self.account = account

        self.table = OperationTableWidget(parent=self)

        title = QtGui.QHBoxLayout()
        title.addWidget(QtGui.QLabel(_(u"Account transactions %(name)s " \
                                       u"(%(number)s)") \
                                     % {'name': self.account.name, \
                                        'number': self.account.number}))

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.table)

        formbox = QtGui.QFormLayout()
        self.order_number = QtGui.QLineEdit()
        self.invoice_number = QtGui.QLineEdit()
        self.invoice_date = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())
        self.invoice_date.setDisplayFormat("yyyy-MM-dd")
        self.provider = QtGui.QLineEdit()
        self.amount = QtGui.QLineEdit()
        self.amount.setValidator(QtGui.QIntValidator())
        butt = QtGui.QPushButton(_(u"Add"))

        formbox1 = QtGui.QHBoxLayout()
        formbox1.addWidget(QtGui.QLabel(_(u'Order number')))
        formbox1.addWidget(QtGui.QLabel(_(u'Invoice number')))
        formbox1.addWidget(QtGui.QLabel(_(u'Invoice date')))
        formbox1.addWidget(QtGui.QLabel(_(u'Provider')))
        formbox1.addWidget(QtGui.QLabel(_(u'Amount')))
        formbox1.addSpacing(90)

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
        vbox.addLayout(hbox)

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
            raise_success(_(u'Confirmation'), _(u'Registered opération'))
            self.refresh()
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


class OperationTableWidget(ANMTableWidget):

    def __init__(self, parent, *args, **kwargs):

        ANMTableWidget.__init__(self, parent=parent, *args, **kwargs)

        # add data
        self.data = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime('%F'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      filter_by(account=self.account).\
                      order_by(desc(Operation.invoice_date)).all()]

        self.setDisplayTotal(True, column_totals={4: None}, \
                             label=_(u"TOTALS"))
        self.period = session.query(Period).first()

        self.header = [_(u'Order number'), _(u'Invoice number'), \
                       _(u'Invoice date'), _(u'Provider'), _(u'Amount')]

        self.refresh()
