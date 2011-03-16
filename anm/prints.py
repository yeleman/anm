#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from sqlalchemy import func, desc

from utils import formatted_number, get_temp_filename
from database import Account, Operation, session
from data_helpers import account_summary
from doclib import Document, Paragraph, Text, Table, Section
from doclib.pdf import PDFGenerator


def build_accounts_report(period, filename=None, format='pdf'):
    ''' PDF: List of balances '''
    if not filename:
        filename = get_temp_filename()

    doc = Document(title=_(u"Accounts balance for %s") \
                         % period.display_name(), landscape=True)

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
    table.set_alignment(Table.ALIGN_RIGHT, column=2)
    table.set_alignment(Table.ALIGN_RIGHT, column=3)

    accounts = [account_summary(account, period) \
                for account in session.query(Account).all()]
    list_budget = []
    list_balance = []
    for account in accounts:
        table.add_row([
            Text(unicode(account[0])),
            Text(unicode(account[1])),
            Text(formatted_number(account[2])),
            Text(formatted_number(account[3]))])
        list_budget.append(account[2])
        list_balance.append(account[3])

    table.add_row([Text(u''),
                   Text(u'TOTALS', bold=True),
                   Text(formatted_number(sum(list_budget)), bold=True),
                   Text(formatted_number(sum(list_balance)), bold=True)])

    doc.add_element(table)

    gen = PDFGenerator(doc, filename)
    gen.render_document()

    return gen.get_filename()


def build_operations_report(account, period, filename=None, format='pdf'):
    ''' PDF: List of operations '''
    doc = Document(title=_(u"The list of operations for the period %s.") \
                         % period.display_name(), \
                           landscape=False, stick_sections=True)

    if account == None:
        accounts = session.query(Account).all()
    else:
        accounts = session.query(Account).\
                           filter_by(number=account.number).all()
    flag = False
    for account in accounts:
        operations = [(operation.order_number, operation.invoice_number,\
                      operation.invoice_date.strftime(u'%x'),\
                      operation.provider, operation.amount, operation) \
                      for operation in session.query(Operation).\
                      filter_by(account=account, period=period).\
                      order_by(desc(Operation.invoice_date)).all()]

        if operations:
            section_name = (_(u'%(name)s (%(number)s)'))\
                               % {'name': account.name,\
                                  'number': account.number}
            doc.add_element(Section(section_name))

            doc.add_element(Paragraph(u''))

            table = Table(5)
            # header row
            table.add_header_row([
                    Text(_(u"Order No.")),
                    Text(_(u"Invoice No.")),
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
            table.set_alignment(Table.ALIGN_RIGHT, column=4)

            list_amount = []
            for operation in operations:
                table.add_row([
                    Text(operation[0]),
                    Text(operation[1]),
                    Text(operation[2]),
                    Text(operation[3]),
                    Text(formatted_number(operation[4]))])
                list_amount.append(operation[4])

            table.add_row([Text(u''),
                           Text(u''),
                           Text(u''),
                           Text(u'TOTAL', bold=True),
                           Text(formatted_number(sum(list_amount)), \
                                bold=True)])

            doc.add_element(table)
            flag = True

    if not flag:
        doc.add_element(Paragraph(\
                Text(_(u'It has no operations for this period.'), bold=True)))

    gen = PDFGenerator(doc, filename)
    gen.render_document()

    return gen.get_filename()
