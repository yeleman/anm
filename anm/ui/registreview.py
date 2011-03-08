#!/usr/bin/env python
# encoding=utf-8
# maintainer: Alou

from PyQt4 import QtGui
from PyQt4 import QtCore

from common import ANMWidget
from database import Period, session
from data_helpers import current_period


class RegistreWidget(ANMWidget):

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
        self.box = QtGui.QComboBox()
        self.box1 = QtGui.QComboBox()
        # Data
        current = current_period()
        self.data = session.query(Period).filter_by(start_on = current.start_on).all()
        self.data1 = ['solde', 'operation']

        for index in xrange(0, len(self.data)):
            ped = self.data[index]
            self.box.addItem('period: %s' % (ped.name) , QtCore.QVariant(ped.id))
        for index in xrange(0, len(self.data1)):
            print index
            pe = self.data1[index]
            print pe
            self.box1.addItem('type: %s' % (pe) , QtCore.QVariant(index))
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
        combo_hbox.addWidget(self.box)
        combo_hbox.addWidget(self.box1)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(combo_hbox)
        vbox.addLayout(button_hbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def capture_ok(self):
        ped = self.data[self.box.currentIndex()]
        pe = self.data1[self.box1.currentIndex()]
        print 'ped %s' % ped
        print 'pe %s' % pe


