#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


import os
import shutil
from datetime import datetime

from PyQt4 import QtGui, QtCore

import database
from database import *
from export_xls import write_xls
from utils import raise_success, raise_error


def export_database_as_file():
    destination = QtGui.QFileDialog.getSaveFileName(QtGui.QWidget(), \
                                    _(u"Save DB as..."), \
                                    "%s.db" % datetime.now().strftime('%c'), \
                                    "*.db")
    if not destination:
        return

    try:
        shutil.copyfile(database.DB_FILE, destination)
        raise_success(_(u"Database exported!"), \
                      _(u"The Database has been successfuly exported.\n" \
                        u"Keep that file private as it contains your data.\n" \
                        u"Export your data regularly."))
    except IOError:
        raise_error(_(u"Error in exporting Database!"), \
                    _(u"The database backup could not be exported.\n" \
                      u"Please verify that you selected a destination " \
                      u"folder which you have write permissions to.\n" \
                      u"Then retry.\n\n" \
                      u"Request assistance if the problem persist."))


def export_database_as_excel():

    destination = QtGui.QFileDialog.getSaveFileName(QtGui.QWidget(), \
                                    _(u"Save Excel Export as..."), \
                                    "%s.xls" % datetime.now().strftime('%c'), \
                                    "*.xls")
    if not destination:
        return

    try:
        shutil.copyfile(write_xls(), destination)
        raise_success(_(u"Database exported!"), \
                      _(u"The data have been successfully exported.\n" \
                        u"Keep that file private as it contains your data.\n" \
                        u"Export your data regularly."))
    except IOError:
        raise_error(_(u"Error in exporting Database!"), \
                    _(u"The database backup could not be exported.\n" \
                      u"Please verify that you selected a destination " \
                      u"folder which you have write permissions to.\n" \
                      u"Then retry.\n\n" \
                      u"Request assistance if the problem persist."))
