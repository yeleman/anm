#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou

from PyQt4 import QtGui
from PyQt4 import QtCore

from sqlalchemy import desc

from datetime import date

from common import ANMWidget, ANMTableWidget, ANMPeriodHolder, ANMPageTitle
from database import Operation, session, Period
from utils import raise_success, raise_error, \
                  date2qdate, qdate2date, formatted_number
from data_helpers import account_balance, period_for, current_period


class OperationWidget(ANMWidget, ANMPeriodHolder):
    def __init__(self, account, period=current_period(), \
                 parent=0, *args, **kwargs):
        super(OperationWidget, self).__init__(parent=parent, *args, **kwargs)
        ANMPeriodHolder.__init__(self, period, *args, **kwargs)

        # set global account
        self.account = account
        self.main_period = period
        self.balance = account_balance(self.account, period)

        self.table = OperationTableWidget(parent=self, period=self.main_period)

        self.title = ANMPageTitle(_(u"Transactions List for Account " \
                                    u"%(number)s: %(name)s.") \
                                    % {'name': self.account.name, \
                                       'number': self.account.number})

        self.balance_title = ANMPageTitle(_(u"Balance: " u"%(balance)s FCFA") \
                                    % {'balance': \
                                              formatted_number(account_balance(self.account, period))})
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.table)

        formbox = QtGui.QFormLayout()
        self.order_number = QtGui.QLineEdit()
        self.invoice_number = QtGui.QLineEdit()
        self.invoice_date = QtGui.QDateTimeEdit(QtCore.QDate.currentDate())
        self.invoice_date.setDisplayFormat("yyyy-MM-dd")
        # change date if appropriate
        self.adjust_date_field()
        self.provider = QtGui.QLineEdit()
        self.amount = QtGui.QLineEdit()
        self.amount.setValidator(QtGui.QIntValidator())
        butt = QtGui.QPushButton(_(u"Add"))
        butt.clicked.connect(self.add_operation)

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

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.balance_title)
        vbox.addWidget(self.periods_bar)
        vbox.addLayout(formbox1)
        vbox.addLayout(formbox)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def add_operation(self):
        ''' add operation '''
        year, month, day = self.invoice_date.text().split('-')
        invoice_date = date(int(year), int(month), int(day))
        period = period_for(invoice_date)

        try:
            amount = int(self.amount.text())
        except ValueError:
            amount = 0

        if self.order_number.text() and self.invoice_number.text() and \
            invoice_date and self.provider.text() and self.amount.text()\
            and invoice_date >= self.main_period.start_on and invoice_date <= \
            self.main_period.end_on and amount < self.balance:
            operation = Operation(unicode(self.order_number.text()),
                        unicode(self.invoice_number.text()), invoice_date, \
                        unicode(self.provider.text()), amount)
            operation.account = self.account
            operation.period = period
            session.add(operation)
            session.commit()
            raise_success(_(u'Confirmation'), _(u'Registered opération'))
            self.order_number.clear()
            self.invoice_number.clear()
            self.provider.clear()
            self.amount.clear()
            self.adjust_balance(period)
            self.refresh()
        elif invoice_date > self.main_period.end_on or\
             invoice_date < self.main_period.start_on:
            raise_error(_(u'Error date'), \
            _(u'The date is not included in the current quarter.'))
        elif amount >= self.balance:
            raise_error(_(u'Error money'),\
             _(u"There is not enough money for this operation."))
        else:
            raise_error(_(u'Error field'), _(u'You must fill in all fields.'))

    def refresh(self):
        self.table.refresh_period(self.main_period)

    def change_period(self, period):
        self.adjust_date_field()
        self.adjust_balance(period)
        self.table.refresh_period(period)

    def adjust_balance(self, period):
        ''' adjusts the balance by period '''
        self.balance = account_balance(self.account, period)
        self.balance_title.setText(_(u"Balance: " u"%(balance)s FCFA") \
                                    % {'balance': \
                                              formatted_number(self.balance)})

    def adjust_date_field(self):
        if period_for(qdate2date(self.invoice_date.date())) ==\
                                                        self.main_period:
            # keep what's on
            return
        if period_for(date.today()) == self.main_period:
            new_date = date.today()
        else:
            new_date = self.main_period.start_on
        self.invoice_date.setDate(new_date)


class OperationTableWidget(ANMTableWidget):

    def __init__(self, parent, period, *args, **kwargs):

        ANMTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.setDisplayTotal(True, column_totals={4: None}, \
                             label=_(u"TOTALS"))

        self.header = [_(u'Order number'), _(u'Invoice number'), \
                       _(u'Invoice date'), _(u'Provider'), _(u'Amount')]

        self.set_data_for(period)

        self.refresh(True)

    def refresh_period(self, period):
        self._reset()
        self.main_period = period
        self.set_data_for(period)
        self.refresh(True)

    def set_data_for(self, period=current_period()):
        self.data = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime(u'%d-%m-%Y'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      filter_by(account=self.account, period=period).\
                      order_by(desc(Operation.invoice_date)).all()]
