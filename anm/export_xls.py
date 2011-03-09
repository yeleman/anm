#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad

import xlwt

from datetime import datetime, date
from sqlalchemy import desc, func

from database import Operation, Account, Period, session, Budget
from data_helpers import account_balance, AccountNotConfigured, data_budget

font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.bold = True
font0.height = 14 * 0x14
font0.underline = xlwt.Font.UNDERLINE_DOUBLE

font1 = xlwt.Font()
font1.name = 'Verdana'
font1.bold = True
font1.height = 10 * 0x14

borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

al = xlwt.Alignment()
al.horz = xlwt.Alignment.HORZ_CENTER
al.vert = xlwt.Alignment.VERT_CENTER

pat2 = xlwt.Pattern()
pat2.pattern = xlwt.Pattern.SOLID_PATTERN
pat2.pattern_fore_colour = 0x01F

style0 = xlwt.XFStyle()
style0.font = font1
style0.borders = borders

style1 = xlwt.XFStyle()
style1.pattern = pat2
style1.borders = borders

style2 = xlwt.XFStyle()
style2.borders = borders

style_title = xlwt.XFStyle()
style_title.font = font0
style_title.alignment = al


def write_xls():
    ''' Export data '''

    book = xlwt.Workbook(encoding='ascii')
    file_name = "base.xls"

    sheet = book.add_sheet(_(u"balance"))
    sheet.write_merge(0, 1, 1, 2,\
                    _(u"The list of accounts per quarter per account"),\
                                                            style_title)
    date_ = _(u"Bamako the %s") % date.today()
    sheet.write(2, 0, unicode(date_))

    hdngs = [_(u"Account Number"), _(u"No Account")]

    rowx1 = 5
    for colx, value in enumerate(hdngs):
        sheet.write(rowx1, colx, value, style0)

    periods = session.query(Period).order_by(Period.start_on).all()
    accounts = session.query(Account).all()

    for account in accounts:
        rowx1 += 1
        sheet.col(colx - 1).width = 0x0d00 * 2
        sheet.col(colx).width = 0x0d00 * 3
        if int(rowx1) % 2 == 0:
            style = style1
        else:
            style = style2
        sheet.write(rowx1, colx - 1, account.number, style)
        sheet.write(rowx1, colx, account.name, style)

        col = 2
        for period  in periods:
            try:
                balance = account_balance(account, period)
                Budget_amount = session.query(Budget.amount).\
                                    filter_by(account=account,\
                                        period=period).scalar()
                if int(rowx1) % 2 == 0:
                    style = style1
                else:
                    style = style2
                sheet.write(rowx1, col, Budget_amount, style)
                sheet.write(rowx1, col + 1, balance, style)
                col += 2
            except AccountNotConfigured:
                pass

    col -= 2
    sheet.write(rowx1 + 1, col - 1, _(u"TOTALS"), style0)
    for nber in range(len(periods)):
        if data_budget(periods[nber]) == True:
            # La somme de tout les operations
            total_op = session.query(func.sum(Operation.amount)).\
                            filter_by(period=periods[nber]).scalar()
            # La somme de tout les budgets
            total_budget = session.query(func.sum(Budget.amount)).\
                            filter_by(period=periods[nber]).scalar()
            # la somme de tout soldes
            total_balance = total_budget - total_op

            sheet.write(rowx1 + 1, col, total_budget, style0)
            sheet.write(rowx1 + 1, col + 1, total_balance, style0)
            col += 2
    col = 2
    for nber in range(len(periods)):
        if data_budget(periods[nber]) == True:
            sheet.col(col).width = 0x0d00 * 2
            sheet.col(col + 1).width = 0x0d00 * 2
            sheet.write_merge(4, 4, col, col + 1,\
                                periods[nber].display_name(), style0)
            sheet.write(5, col, _(u"Budget"), style0)
            sheet.write(5, col + 1, _(u"Balance"), style0)
            col += 2

    # Pour les operations
    for account in accounts:
        sheet_name = account.number

        sheet = book.add_sheet(sheet_name)
        rowx = 1
        sheet.write_merge(0, rowx, 1, 3, \
                                _(u"List of transaction per quarter"),\
                                style_title)
        rowx += 2
        account_name = _(u"Account: %s") % account.name
        sheet.write_merge(rowx, rowx, 1, 3, account_name, style_title)
        for period  in periods:
            operations = [(operation.order_number, operation.invoice_number,\
                            operation.invoice_date.strftime('%F'),\
                            operation.provider, operation.amount) \
                            for operation in session.query(Operation).\
                            filter_by(account=account, period=period).\
                            order_by(desc(Operation.invoice_date)).all()]
            if operations:
                sheet.write_merge(rowx + 2, rowx + 2, 1, 2,\
                                    period.display_name(), style_title)
                hdngs = [_(u"No mandate"), _(u"No invoice"),\
                         _(u"Invoice Date"), _(u"Provider"),\
                                             _(u"Amount")]
                rowx += 4
                for colx, value in enumerate(hdngs):
                    sheet.write(rowx, colx, value, style0)
                    sheet.col(colx).width = 0x0d00 * 2
                amount_opera = 0
                for row in operations:
                    rowx += 1
                    if int(rowx) % 2 == 0:
                        style = style1
                    else:
                        style = style2
                    for colx, value in enumerate(row):
                        sheet.write(rowx, colx, value, style)
                    amount_opera += row[4]
                # On fait le total du montant des operations par teimestre
                sheet.write(rowx + 1, colx - 1, _(u"TOTAL"), style0)
                sheet.write(rowx + 1, colx, amount_opera, style0)
                rowx += 1
            else:
                sheet.col(2).width = 0x0d00 * 2
                sheet.col(1).width = 0x0d00 * 2
                rowx += 2
                sheet.write_merge(rowx, rowx, 1, 2,\
                                    period.display_name(), style_title)
                rowx += 2
                sheet.write_merge(rowx, rowx, 1, 2,\
                                    _(u"This account has no record"))
                rowx += 1

    book.save(file_name)
    return file_name
