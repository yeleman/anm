#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

import xlwt

from datetime import datetime, date
from sqlalchemy import func, desc

from database import Operation, Account, Period, session
from data_helpers import *

font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.bold = True

style0 = xlwt.XFStyle()
style0.font = font0


def write_xls():
    ''' Export data '''

    book = xlwt.Workbook(encoding='ascii')
    file_name = "exports_excel.xls"

    sheet = book.add_sheet(_(u"balance"))
    sheet.write(1, 1, _(u"The list of accounts per quarter per account"),\
                                        style0)
    date_ = _(u"Bamako the %s") % date.today()
    sheet.write(2, 5, unicode(date_))

    hdngs = [u"Numéro Compte", u"Non Compte"]

    rowx1 = 5
    for colx, value in enumerate(hdngs):
        sheet.write(rowx1, colx, value, style0)

    periods = session.query(Period).all()
    accounts = session.query(Account).all()

    for account in accounts:
        rowx1 += 1
        sheet.write(rowx1, colx, account.name)
        sheet.write(rowx1, colx - 1, account.number)
        col = 5
        for period  in periods:

            balance = account_balance(account, period)

            data1 = [(budget.amount) for budget in session.query(Budget).\
                        filter_by(account=account, period=period).all()]

            sheet.write(rowx1, col, budget.amount)
            sheet.write(rowx1, col + 1, balance)
            col += 2

    col = 5
    for nber in range(len(periods)):
        sheet.write(4, col, period.name)
        sheet.write(5, col, _(u"Budget"), style0)
        sheet.write(5, col + 1, _(u"Balance"), style0)
        col += 2

    # Pourles operations
    for account in session.query(Account).all():
        sheet_name = account.number

        sheet = book.add_sheet(sheet_name)
        rowx = 0
        for period  in session.query(Period).all():

            data = [(operation.order_number, operation.invoice_number, \
                        operation.invoice_date.strftime('%F'),\
                        operation.provider, operation.amount) \
                        for operation in session.query(Operation).\
                        filter_by(account=account, period=period).\
                        order_by(desc(Operation.invoice_date)).all()]
            if data:
                sheet.write(rowx + 1, 2, period.name, style0)
                hdngs = [u"No mandat", u"No Facture", u"Date Facture",\
                                            u"Fournisseur", u"Montant"]

                rowx += 3
                for colx, value in enumerate(hdngs):
                    sheet.write(rowx, colx, value, style0)

                sheet.set_panes_frozen(True)
                sheet.set_horz_split_pos(rowx)
                sheet.set_horz_split_pos(rowx + 1)
                sheet.set_remove_splits(True)

                for row in data:
                    rowx += 1
                    for colx, value in enumerate(row):
                        sheet.write(rowx, colx, value)
                rowx += 1
            else:
                rowx += 1
                sheet.write(rowx, 2, period.name, style0)
                rowx += 1
                sheet.write(rowx, 1, _(u"This account has no record"),\
                                        style0)
                rowx += 1

    book.save(file_name)
