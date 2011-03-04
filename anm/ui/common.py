#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui

class ANMWidget(QtGui.QWidget):

    def __init__(self, parent=0, *args, **kwargs):

        QtGui.QWidget.__init__(self, parent=parent, *args, **kwargs)

    def refresh(self):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        return self.parentWidget()\
                          .change_context(context_widget, *args, **kwargs)

    def getaccount(self):
        return self.parentWidget().account

    def setaccount(self, value):
        self.parentWidget().account = value
    
    def clear_account(self):
        self.parentWidget().account = None

    account = property(getaccount, setaccount)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(dialog, \
                                               modal=modal, *args, **kwargs)
