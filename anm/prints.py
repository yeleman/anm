#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from gettext import gettext as _

from database import Account, Operation, session
from data_helpers import account_summary
from doclib import *
from doclib.pdf import PDFGenerator
from sqlalchemy import func, desc


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


def build_operations_report(account, period, filename=None, format='pdf'):

    doc = Document(title=_(u"List operations for %s") % period, \
                   landscape=False)

    table = Table(5)
    table.add_header_row([
            Text(_(u"Order number")),
            Text(_(u"Invoice number")),
            Text(_(u"Invoice date")),
            Text(_(u"Provider")),
            Text(_(u"Amount"))])

    # column widths
    table.set_column_width(10, 0)
    table.set_column_width(10, 1)
    table.set_column_width(15, 2)
    table.set_column_width(15, 4)

    # column alignments
    table.set_alignment(Table.ALIGN_LEFT, column=0)
    table.set_alignment(Table.ALIGN_LEFT, column=1)
    table.set_alignment(Table.ALIGN_LEFT, column=2)
    table.set_alignment(Table.ALIGN_LEFT, column=3)
    table.set_alignment(Table.ALIGN_LEFT, column=4)
    if account == None:
        operations = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime('%F'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      group_by(Operation.account).\
                      order_by(desc(Operation.invoice_date)).all()]

    else:
        operations = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime('%F'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      filter_by(account=account, period=period).\
                      order_by(desc(Operation.invoice_date)).all()]

    if operations:
        for operation in operations:
            table.add_row([
                Text(operation[0]),
                Text(operation[1]),
                Text(operation[2]),
                Text(operation[3]),
                Text(operation[4])])

        doc.add_element(table)

    gen = PDFGenerator(doc, filename)
    gen.render_document()
    return gen.get_filename()
