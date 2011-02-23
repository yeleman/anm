#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
from PyQt4 import QtGui

class BalanceViewWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel("List of account's balances"))

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
