#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
import gettext
import locale

from PyQt4 import QtGui

import fixture_data
import gettext_windows
from ui import MainWindow
from ui.window import ANMWindow


def main():

    gettext_windows.setup_env()

    locale.setlocale(locale.LC_ALL, '')

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
