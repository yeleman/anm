#!/usr/bin/env python
# encoding=utf-8
# maintainer: Tief

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from sqlalchemy import desc

from utils import raise_error, raise_success
from common import ANMWidget
from database import Operation, session
from data_helpers import current_period


class deleteViewWidget(QtGui.QDialog, ANMWidget):

    def __init__(self, parent, account, *args, **kwargs):
        QtGui.QDialog.__init__(self, parent, *args, **kwargs)

        # set global account
        self.account = account

        self.setWindowTitle(_(u"Delete an operation"))

        #Title widget
        title = QtGui.QLabel()
        title.setText(_(u"Select an operation to delete"))
        title.setAlignment(Qt.AlignHCenter)
        title_hbox = QtGui.QHBoxLayout()
        title_hbox.addWidget(title)

        #Combobox widget
        self.box = QtGui.QComboBox()

        #Fill Combobox.
        self.data = session.query(Operation).\
                      filter_by(account=self.account, period=current_period()).\
                      order_by(desc(Operation.invoice_date)).all()

        if self.data != []:
            for index in xrange(0, len(self.data)):
                op = self.data[index]
                part1 = u"order number: %s, invoice number: %s, provider: %s," %\
                    (op.order_number, op.invoice_number,\
                     op.provider)
                part2 = u"amount: %s, invoice date: %s" % (op.amount,\
                    op.invoice_date.strftime('%F'))
                sentence = part1 + part2
                self.box.addItem(sentence, QtCore.QVariant(op.id))
            combo_hbox = QtGui.QHBoxLayout()
            combo_hbox.addWidget(self.box)
        else:
            raise_error(_(u'Delete error'), _(u'Not operation to delete !'))

        #delete and cancel hbox
        button_hbox = QtGui.QHBoxLayout()

        #Delete Button widget.
        delete_but = QtGui.QPushButton(_("Delete operation"))
        button_hbox.addWidget(delete_but)
        delete_but.clicked.connect(self.delete)

        #Cancel Button widget.
        cancel_but = QtGui.QPushButton(_("Cancel"))
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
        raise_success(_(u'Deleting'), _(u'Operation succefully removed'))
        self.box.removeItem(self.box.currentIndex())
