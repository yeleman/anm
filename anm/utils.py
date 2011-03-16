#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os
import sys
import locale
import tempfile
import subprocess
from datetime import date

from PyQt4 import QtGui, QtCore

from ui.window import ANMWindow


class PDFFileUnavailable(IOError):
    pass


def uopen_prefix(platform=sys.platform):

    if platform in ('win32', 'win64'):
        return 'cmd /c start'

    if 'darwin' in platform:
        return 'open'

    if platform in ('cygwin', 'linux') or \
       platform.startswith('linux') or \
       platform.startswith('sun') or \
       'bsd' in platform:
        return 'xdg-open'

    return 'xdg-open'


def uopen_file(filename):
    if not os.path.exists(filename):
        raise IOError(_(u"File %s is not available.") % filename)
    subprocess.call('%(cmd)s %(file)s' \
                    % {'cmd': uopen_prefix(), 'file': filename}, shell=True)


def display_pdf(pdf_file):
    try:
        return uopen_file(pdf_file)
    except IOError:
        raise PDFFileUnavailable(_(u"PDF file %s is not available.") \
                                 % pdf_file)


def raise_error(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Critical, title, \
                            message, QtGui.QMessageBox.Ok, \
                            parent=ANMWindow.window)
    box.exec_()


def raise_success(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Information, title, \
                            message, QtGui.QMessageBox.Ok, \
                            parent=ANMWindow.window)
    box.exec_()


def formatted_number(number):
    try:
        return locale.format("%d", number, grouping=True) \
                     .decode(locale.getlocale()[1])
    except:
        return "%s" % number


def get_temp_filename():
    f = tempfile.NamedTemporaryFile(delete=False)
    return f.name

def date2qdate(adate):
    ''' returns a date object from a QtCore.QDate '''
    return QtCore.QDate(adate.year, adate.month, adate.day)


def qdate2date(adate):
    ''' returns a QtCore.QDate from a date object '''
    return date(adate.year(), adate.month(), adate.day())
