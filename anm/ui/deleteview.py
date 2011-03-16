#!/usr/bin/env python
# encoding=utf-8
# maintainer: Tief

from PyQt4 import QtGui
from PyQt4 import QtCore

from sqlalchemy import desc

from utils import raise_error, raise_success
from common import ANMWidget
from database import Operation, session
from data_helpers import current_period
from operationview import OperationWidget


class deleteViewWidget(QtGui.QDialog, ANMWidget):

    def __init__(self, parent, account, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)

        #Fill Combobox.
        self.data = session.query(Operation).\
                    filter_by(account=self.account, period=current_period()).\
                    order_by(desc(Operation.invoice_date)).all()

        if self.data == []:
            title = QtGui.QLabel()
            title.setText(_(u"there is no operation"))
            ok_butt = QtGui.QPushButton(_(u"OK"))
            ok_butt.clicked.connect(self.close)

            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(title)
            vbox.addWidget(ok_butt)
            self.setLayout(vbox)
        else:
            # set global account
            self.account = account
            self.setWindowTitle(_(u"Delete an operation"))
            #Title widget
            title = QtGui.QLabel()
            title.setText(_(u"Select an operation to delete"))
            title.setAlignment(QtCore.Qt.AlignHCenter)
            title_hbox = QtGui.QHBoxLayout()
            title_hbox.addWidget(title)

            #Combobox widget
            self.box = QtGui.QComboBox()
            for index in xrange(0, len(self.data)):
                op = self.data[index]
                sentence = \
                    _(u"L'operation which has for n° mandate %(order_num)s,"\
                        u" n° invoice %(invoice_num)s, "\
                        u"date invoices %(date)s, Provider %(provider)s"\
                        u" and of amount %(amount)s") \
                        % {'order_num': op.order_number, \
                             'invoice_num': op.invoice_number, \
                             'provider': op.provider, 'amount': op.amount, \
                             'date': op.invoice_date.strftime('%x')}
                self.box.addItem(sentence, QtCore.QVariant(op.id))

            combo_hbox = QtGui.QHBoxLayout()
            combo_hbox.addWidget(self.box)

            #delete and cancel hbox
            button_hbox = QtGui.QHBoxLayout()

            #Delete Button widget.
            delete_but = QtGui.QPushButton(_(u"Delete operation"))
            button_hbox.addWidget(delete_but)
            delete_but.clicked.connect(self.delete)
            #Cancel Button widget.
            cancel_but = QtGui.QPushButton(_(u"Cancel"))
            button_hbox.addWidget(cancel_but)
            cancel_but.clicked.connect(self.cancel)

            #Create the QVBoxLayout contenaire.
            vbox = QtGui.QVBoxLayout()
            vbox.addLayout(title_hbox)
            vbox.addLayout(combo_hbox)
            vbox.addLayout(button_hbox)
            self.setLayout(vbox)

    def cancel(self):
        self.close()

    def delete(self):
        op = self.data[self.box.currentIndex()]
        session.delete(op)
        session.commit()
        self.change_main_context(OperationWidget, account=self.account)
        self.box.removeItem(self.box.currentIndex())
        if len(self.data) == 1:
            self.close()
        else:
            self.data.pop(self.box.currentIndex())
        raise_success(_(u"Deleting"), _(u"Operation succefully removed"))
