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


class ANMTableWidget(QtGui.QTableWidget):

    def __init__(self, parent, *args, **kwargs):

        QtGui.QTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self._data = []
        self._header = []
        self.parent = parent

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)


        self.cellClicked.connect(self.click_item)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setFont(QtGui.QFont("Courier New", 10))

    def setdata(self, value):
        if not isinstance(value, (list, None.__class__)):
            raise ValueError
        self._data = value

    def getdata(self):
        return self._data

    data = property(getdata, setdata)

    def setheader(self, value):
        if not isinstance(value, (list, None.__class__)):
            raise ValueError
        self._header = value

    def getheader(self):
        return self._header

    header = property(getheader, setheader)

    def refresh(self):
        if not self.data or not self.header:
            return

        self.setRowCount(self.data.__len__())
        self.setColumnCount(self.header.__len__())
        self.setHorizontalHeaderLabels(self.header)

        n = 0
        for row in self.data:
            m = 0
            for item in row:
                if m == row.__len__() - 1:
                    newitem = QtGui.QTableWidgetItem(\
                                    QtGui.QIcon("images/go-next.png"), \
                                    _(u""))
                else:
                    newitem = QtGui.QTableWidgetItem(u"%s" % item)
                self.setItem(n, m, newitem)
                m += 1
            n += 1

        self.resizeColumnsToContents()

    def  click_item(self, row, column, *args):
        pass
