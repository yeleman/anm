#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import locale

from PyQt4 import QtGui
from PyQt4.QtCore import Qt


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


class ANMTableWidget(QtGui.QTableWidget, ANMWidget):

    def __init__(self, parent, *args, **kwargs):

        QtGui.QTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self._data = []
        self._header = []
        self._display_total = False
        self._column_totals = {}
        self._total_label = _(u"TOTAL")

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

        # increase rowCount by one if we have to display total row
        rc = self.data.__len__()
        if self._display_total:
            rc += 1
        self.setRowCount(rc)
        self.setColumnCount(self.header.__len__())
        self.setHorizontalHeaderLabels(self.header)

        n = 0
        for row in self.data:
            m = 0
            for item in row:
                if m == row.__len__() - 1:
                    newitem = QtGui.QTableWidgetItem(\
                                    QtGui.QIcon("images/go-next.png"), '')
                else:
                    newitem = QtGui.QTableWidgetItem(\
                                                  self._format_for_table(item))
                self.setItem(n, m, newitem)
                m += 1
            n += 1

        self._display_total_row()

        self.resizeColumnsToContents()

    def _display_total_row(self, row_num=None):
        ''' adds the total row at end of table '''

        # display total row at end of table
        if self._display_total:

            if not row_num:
                row_num = self.data.__len__()

            # spans columns up to first data one
            # add label inside
            label_item = QtGui.QTableWidgetItem(u"%s" % self._total_label)
            label_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setItem(row_num, 0, label_item)
            self.setSpan(row_num, 0, 1, self._column_totals.keys()[0])
            # calculate total for each total column
            # if desired
            for index, total in self._column_totals.items():
                if not total:
                    total = sum([data[index] for data in self.data])
                item = QtGui.QTableWidgetItem(self._format_for_table(total))
                self.setItem(row_num, index, item)

    def setDisplayTotal(self, display=False, \
                              column_totals={}, \
                              label=None):
        ''' adds an additional row at end of table

        display: bool wheter of not to display the total row
        column_totals: an hash indexed by column number
                       providing data to display as total or None
                       to request automatic calculation
        label: text of first cell (spaned up to first index)
        Example call:
            self.setDisplayTotal(True, \
                                 column_totals={2: None, 3: None}, \
                                 label="TOTALS") '''

        self._display_total = display
        self._column_totals = column_totals
        if label:
            self._total_label = label

    def _format_for_table(self, value):
        ''' formats input value for string in table widget '''
        if isinstance(value, basestring):
            return value

        if isinstance(value, (int, float, long)):
            return locale.format("%d", value, grouping=True)

        return u"%s" % value

    def  click_item(self, row, column, *args):
        pass
