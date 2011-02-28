#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou
#!/usr/bin/env python
# encoding=utf-8

import re
import operator

from database import Operation, session
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import *
from sqlalchemy import desc
#~ from balanceview import BalanceViewWidget


class deleteViewWidget(QtGui.QDialog):

    def __init__(self, account):
        QtGui.QDialog.__init__(self)
        self.account = account
        print self.account
        self.setWindowTitle(_(u"Delete an operation"))

        #Title widget
        title = QtGui.QLabel()
        title.setText(_(u"Select an operation to delete"))
        title_hbox = QtGui.QHBoxLayout()
        title_hbox.addWidget(title)
        
        #Combobox widget
        self.box = QtGui.QComboBox()
        self.box.setEditable(False)
        
        #Fill Combobox.
        self.data = session.query(Operation).\
                      filter_by(account=self.account).\
                      order_by(desc(Operation.invoice_date)).all()
        
        for index in xrange(0, len(self.data)):
            op = self.data[index]
            self.box.addItem(u"%s %s %s %s %s" % (op.order_number, op.invoice_number, op.invoice_date.strftime('%F'), op.provider, op.amount), QtCore.QVariant(op.id))
        combo_hbox = QtGui.QHBoxLayout()
        combo_hbox.addWidget(self.box)

        #Delete Button widget.
        delete_but = QtGui.QPushButton("Delete operation")
        delete_hbox = QtGui.QHBoxLayout()
        delete_hbox.addWidget(delete_but)
        
        delete_but.clicked.connect(self.delete)
        
        #Cancel Button widget.
        cancel_but = QtGui.QPushButton("Cancel")
        cancel_hbox = QtGui.QHBoxLayout()
        cancel_hbox.addWidget(cancel_but)
        cancel_but.clicked.connect(self.cancel)
        
        #Create the QVBoxLayout contenaire.
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(combo_hbox)
        vbox.addLayout(delete_hbox)
        vbox.addLayout(cancel_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
 
    def cancel(self):
        self.close()
    
    def delete(self):
        print self.box.currentIndex()
        op = self.data[self.box.currentIndex()]
        session.delete(op)
        session.commit()
        self.box.removeItem(self.box.currentIndex())
        
