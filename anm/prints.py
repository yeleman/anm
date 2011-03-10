#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import locale

from gettext import gettext as _

from sqlalchemy import func, desc

from database import Account, Operation, session
from data_helpers import account_summary
from doclib import Document, Paragraph, Text, Table, Section
from doclib.pdf import PDFGenerator



def build_accounts_report(period, filename=None, format='pdf'):
    """ PDF: List of balances """

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
    list_budget= []
    list_balance= []
    for account in accounts:
        table.add_row([
            Text(account[0]),
            Text(account[1]),
            Text(locale.format("%d", account[2], grouping=True)),
            Text(locale.format("%d", account[3], grouping=True))])
        list_budget.append(account[2])
        list_balance.append(account[3])

    table.add_row([Text(''),
                   Text('TOTALS', bold=True),
                   Text(locale.format("%d", sum(list_budget),
                                      grouping=True), bold=True),
                   Text(locale.format("%d", sum(list_balance),
                                      grouping=True), bold=True)])

    doc.add_element(table)

    gen = PDFGenerator(doc, filename)
    gen.render_document()

    return gen.get_filename()


def build_operations_report(account, period, filename=None, format='pdf'):
    """ PDF: List of operations """
    doc = Document(title=_(u"The list of operations for the period %s.") \
                    % period, landscape=False, stick_sections=True)

    if account == None:
        accounts = session.query(Account).all()
    else:
        accounts = session.query(Account).filter_by(number=account.number).all()
    flag = False
    for account in accounts:
        operations = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime('%F'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      filter_by(account=account, period=period).\
                      order_by(desc(Operation.invoice_date)).all()]

        if operations:
            section_name = (_('%(name)s (%(number)s)'))\
                               % {'name': account.name,\
                                  'number': account.number}
            doc.add_element(Section(section_name))

            doc.add_element(Paragraph(u''))

            table = Table(5)
            # header row
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

            list_amount= []
            for operation in operations:
                table.add_row([
                    Text(operation[0]),
                    Text(operation[1]),
                    Text(operation[2]),
                    Text(operation[3]),
                    Text(locale.format("%d", operation[4], grouping=True))])
                list_amount.append(operation[4])

            table.add_row([Text(''),
                           Text(''),
                           Text(''),
                           Text('TOTAL', bold=True ),
                           Text(locale.format("%d", sum(list_amount),\
                                              grouping=True), bold=True)])

            doc.add_element(table)
            flag = True

    if not flag:
        doc.add_element(Paragraph(\
                Text(_(u'It has no operations for this period.'), bold=True)))

    gen = PDFGenerator(doc, filename)
    gen.render_document()

    return gen.get_filename()
