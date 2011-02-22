#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
from PyQt4 import QtGui, QtCore

class MenuBar(QtGui.QMenuBar):

    def __init__(self, parent=None):
        QtGui.QMenuBar.__init__(self, parent)
        #menubar = self.menuBar()

        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        self.connect(exit, QtCore.SIGNAL('triggered()'), \
                                         self.parentWidget(), \
                                         QtCore.SLOT('close()'))

        file_ = self.addMenu('&File')
        file_.addAction(exit)
