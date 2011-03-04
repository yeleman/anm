#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os
import sys
import subprocess

from PyQt4 import QtGui, QtCore


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
                            message, QtGui.QMessageBox.Ok)
    box.exec_()


def raise_success(title, message):
    box = QtGui.QMessageBox(QtGui.QMessageBox.Information, title, \
                            message, QtGui.QMessageBox.Ok)
    box.exec_()
