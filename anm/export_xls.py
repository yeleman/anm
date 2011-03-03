#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

import xlwt
from datetime import datetime, date
ezxf = xlwt.easyxf
from sqlalchemy import func, desc
from database import Operation, Account, Period, session
from data_helpers import *


def write_xls():
    ''' Export data '''

    book = xlwt.Workbook(encoding='ascii')
    file_name = "exports_excel.xls"

    heading_xf = ezxf('font: bold on; align: wrap on, vert centre,\
                        horiz center')

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
                sheet.write(rowx + 1, 2, period.name)
                hdngs = ['No mandat', 'No Facture', \
                        'Date Facture', 'Fournisseur', 'Montant']

                rowx += 3
                for colx, value in enumerate(hdngs):
                    sheet.write(rowx, colx, value, heading_xf)

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
                sheet.write(rowx, 2, period.name)
                rowx += 1
                sheet.write(rowx, 1, u"This account has no record")
                rowx += 1

    book.save(file_name)
