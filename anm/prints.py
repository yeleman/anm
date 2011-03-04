#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from gettext import gettext as _

from database import *
from data_helpers import account_summary
from doclib import *
from doclib.pdf import PDFGenerator


def build_accounts_report(period, filename=None, format='pdf'):

    doc = Document(title=_(u"Accounts balance for %s") % period, \
                   landscape=True)

    table = Table(4)
    table.add_header_row([
            Text(_(u"Account Number")),
            Text(_(u"Account Name")),
            Text(_(u"Budget")),
            Text(_(u"Balance"))])

    # column widths
    table.set_column_width(10, 0)
    table.set_column_width(15, 2)
    table.set_column_width(15, 3)

    # column alignments
    table.set_alignment(Table.ALIGN_LEFT, column=0)
    table.set_alignment(Table.ALIGN_LEFT, column=1)
    table.set_alignment(Table.ALIGN_LEFT, column=2)
    table.set_alignment(Table.ALIGN_LEFT, column=3)

    accounts = [account_summary(account, period) \
                for account in session.query(Account).all()]
    for account in accounts:
        table.add_row([
            Text(account[0]),
            Text(account[1]),
            Text(account[2]),
            Text(account[3])])

    doc.add_element(table)

    gen = PDFGenerator(doc, filename)
    gen.render_document()
    return gen.get_filename()
