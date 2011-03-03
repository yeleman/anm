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
    i = 0
    file_name = "export_excel.xls"
    heading_xf = ezxf('font: bold on; align: wrap on, vert centre,\
                        horiz center')

    for account in session.query(Account).all():
        i += 1

        sheet_name = account.number
        sheet = book.add_sheet(sheet_name)

        for period  in session.query(Period).all():

            data = [(operation.order_number, operation.invoice_number, \
                        operation.invoice_date.strftime('%F'),\
                        operation.provider, operation.amount) \
                        for operation in session.query(Operation).\
                        filter_by(account=account).\
                        order_by(desc(Operation.invoice_date)).all()]

            sheet.write(1, 2, period.name)
            hdngs = ['No mandat', 'No Facture', \
                    'Date Facture', 'Fournisseur', 'Montant']
            rowx = 3
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

    book.save(file_name)
