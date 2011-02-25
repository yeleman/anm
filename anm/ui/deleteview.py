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

from balanceview import BalanceViewWidget


class deleteViewWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        #Title widget
        title = QtGui.QLabel()
        title.setText(u"Suppression opération")
        title_hbox = QtGui.QHBoxLayout()
        title_hbox.addWidget(title)
        
        #Combobox widget
        self.box = QtGui.QComboBox()
        self.box.setEditable(True)
        #Fill Combobox.
        
        self.data = session.query(Operation).all()
        
        for index in xrange(0, len(self.data)):
            op = self.data[index]
            self.box.addItem(u"%s %s %s %s %s" % (op.order_number, op.invoice_number, op.invoice_date.strftime('%F'), op.provider, op.amount), QtCore.QVariant(op.id))
        combo_hbox = QtGui.QHBoxLayout()
        combo_hbox.addWidget(self.box)

        #Delete Button widget.
        delete_but = QtGui.QPushButton("Delete")
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
        self.parentWidget().switch_context(BalanceViewWidget())
    
    def delete(self):
        print self.box.currentIndex()
        op = self.data[self.box.currentIndex()]
        session.delete(op)
        session.commit()
        self.box.removeItem(self.box.currentIndex())
        
