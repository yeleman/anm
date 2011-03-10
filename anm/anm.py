#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

import gettext
from PyQt4 import QtGui

import fixture_data
from ui import MainWindow
from ui.window import ANMWindow


def main():
    gettext.install('anm', localedir='locale', unicode=True)

    # ensure DB is in place
    fixture_data.initial_setup()

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    setattr(ANMWindow, 'window', window)
    window.show()
    #window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
