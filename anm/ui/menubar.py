#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore

from common import ANMWidget
from balanceview import BalanceViewWidget
from balanceupdateview import BalanceUpdateWidget
from deleteview import deleteViewWidget
from registreview import RegistreWidget
from exports import export_database_as_file, export_database_as_excel
from export_xls import *
from prints import build_accounts_report
from utils import uopen_file


class MenuBar(QtGui.QMenuBar, ANMWidget):

    def __init__(self, parent=None, *args, **kwargs):
        QtGui.QMenuBar.__init__(self, parent, *args, **kwargs)

        #Menu File
        file_ = self.addMenu(_(u"&File"))
        # Dele
        self.delete_ = QtGui.QAction(_(u"Delete an operation"), self)
        self.connect(self.delete_, QtCore.SIGNAL("triggered()"),\
                                            self.goto_delete_operation)
        self.delete_.setEnabled(False)
        file_.addAction(self.delete_)

        # Print
        print_ = QtGui.QAction(_(u"Print"), self)
        print_.setShortcut("Ctrl+P")
        self.connect(print_, QtCore.SIGNAL("triggered()"),\
                                            self.goto_print)
        file_.addAction(print_)
        # Export
        export = file_.addMenu(_(u"Export data"))
        export.addAction(_(u"DB"), self.goto_export_db)
        export.addAction(_(u"Export an file excel"),\
                                        self.goto_export_excel)
        # Exit
        exit = QtGui.QAction(_(u"Exit"), self)
        exit.setShortcut("Ctrl+Q")
        exit.setToolTip(_("Exit application"))
        self.connect(exit, QtCore.SIGNAL("triggered()"), \
                                         self.parentWidget(), \
                                         QtCore.SLOT("close()"))
        file_.addAction(exit)
        # Menu aller à
        goto = self.addMenu(_(u"&Go to"))
        goto.addAction(_(u"Accounts balances"),\
                                    self.goto_Accounts_balances)
        goto.addAction(_(u"Update periodic budgets"),\
                                       self.goto_updated_budget)
        #Menu Aide
        help = self.addMenu(_(u"Help"))
        help.addAction(_(u"About"), self.goto_about)

    #Refresh the menu bar to enabled or disabled the delete menu
    def refresh(self):
        self.delete_.setEnabled(bool(self.parentWidget().account))

    #Print
    def goto_print(self):
        self.open_dialog(RegistreWidget, modal=True)

    #Delete an operation.
    def goto_delete_operation(self):
        self.open_dialog(deleteViewWidget, modal=True, account=self.account)

    #Export the database.
    def goto_export_db(self):
        export_database_as_file()

    def goto_export_excel(self):
        print "export an file excel"
        export_database_as_excel()

    #list_of_balances
    def goto_Accounts_balances(self):
        self.change_main_context(BalanceViewWidget)

    #mise à jour de budget
    def goto_updated_budget(self):
        self.change_main_context(BalanceUpdateWidget)

    #About
    def goto_about(self):
        mbox = QtGui.QMessageBox.about(self.parentWidget(), _(u"About ANM"), \
                          _(u"ANM Budget Management Software\n\n" \
                            u"© 2011 yɛlɛman s.à.r.l\n" \
                            u"Hippodrome, Avenue Al Quds, \n" \
                            u"BPE. 3713 - Bamako (Mali)\n" \
                            u"Tel: (223) 76 33 30 05\n" \
                            u"www.yeleman.com\n" \
                            u"info@yeleman.com\n\n" \
                            u"Aboubacar Diarra, Ali Touré, \n" \
                            u"Alou Dolo, Ibrahima Fadiga, \n" \
                            u"Renaud Gaudin, Tiefolo Doumbia"))
