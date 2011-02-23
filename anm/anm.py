#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

import gettext
from PyQt4 import QtGui

from ui import MainWindow


def main():
    gettext.install('anm', localedir='locale', unicode=True)
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
