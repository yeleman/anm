#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore

from balanceview import BalanceViewWidget


class MenuBar(QtGui.QMenuBar):

    def __init__(self, parent=None):
        QtGui.QMenuBar.__init__(self, parent)

        #Menu File
        file_ = self.addMenu(_(u"&File"))
        # Dele
        file_.addAction(_(u"Delete an operation"),\
                                     self.goto_delete_operation)
        # Print
        print_ = QtGui.QAction(_(u"Print"), self)
        print_.setShortcut("Ctrl+P")
        print_.setDisabled(True)
        self.connect(print_, QtCore.SIGNAL("triggered()"),\
                                            self.goto_print)
        file_.addAction(print_)
        # Export
        export = file_.addMenu(_(u"Export data"))
        export.addAction(_(u"Db"), self.goto_export_db)
        export.addAction(_(u"Export an file excel"),\
                                        self.goto_export_excel)
        # Exit
        exit = QtGui.QAction(_(u"Exit"), self)
        exit.setShortcut("Ctrl+Q")
        exit.setToolTip(_('Exit application'))
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

    #Print
    def goto_print(self):
        print "Processing a Print Request"

    def goto_delete_operation(self):
        print "deleted"

    def goto_export_db(self):
        print "export db"

    def goto_export_excel(self):
        print "export an file excel"

    #list_of_balances
    def goto_Accounts_balances(self):
        self.parentWidget().switch_context(BalanceViewWidget())

    #mise à jour de budget
    def goto_updated_budget(self):
        print "updated budget"

    #About
    def goto_about(self):
        print "About"
