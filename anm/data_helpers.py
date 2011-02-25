#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date, datetime

import sqlalchemy
from sqlalchemy import desc, func
from sqlalchemy.orm import exc
from gettext import gettext as _

from database import *


class AccountNotConfigured(Exception):
    pass


def account_balance(account, period):
    ''' balance amount for a period '''
    expenses = account_expenses(account, period)
    budget = account_budget(account, period)

    balance = budget - expenses
    return balance


def account_expenses(account, period):
    ''' total amount expendited during that period '''
    total = session.query(func.sum(Operation.amount))\
                   .filter_by(account=account)\
                   .filter(func.strftime('%s', Operation.invoice_date) \
                           > period.start_on.strftime('%s'))\
                   .filter(func.strftime('%s', Operation.invoice_date) \
                           < period.end_on.strftime('%s'))\
                   .scalar()
    if total:
        return total
    else:
        return 0


def account_budget(account, period):
    ''' donated budget for a period '''
    try:
        budget = session.query(Budget)\
                        .filter_by(period=period, account=account).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        raise AccountNotConfigured(account)
    return budget.amount


def account_summary(account, period):
    ''' tuple of useful data regarding an account '''
    budget = account_budget(account, period)
    balance = account_balance(account, period)

    return (account.number, account.name, budget, balance, account)


def period_for(date_):
    ''' period object a date is part of '''
    quarter = quarter_for(date_)
    try:
        period = [period for period in \
                  session.query(Period)\
                         .filter(func.strftime('%Y', Period.start_on) \
                                 == date_.strftime('%Y'))\
                         .all() if period.quarter == quarter][0]
    except IndexError:
        start, end = quarter_dates(quarter, date_.year)
        period = Period(name=_(u"Q%(quar)d %(year)d") \
                             % {'quar': quarter, 'year': date_.year}, \
                        start_on=start, end_on=end)
        session.add(period)
        session.commit()
    return period


def quarter_for(date_):
    ''' returns quarter a date is part of '''
    if date_ < date(date_.year, 4, 1):
        return 1
    if date_ < date(date_.year, 7, 1):
        return 2
    if date_ < date(date_.year, 10, 1):
        return 3
    return 4


def next_quarter(quarter, year=None):
    ''' return next quarter number '''
    if quarter < 4:
        return (quarter + 1, year)
    return (1, year + 1)


def previous_quarter(quarter, year=None):
    ''' return next quarter number '''
    if quarter > 1:
        return (quarter - 1, year)
    return (4, year - 1)


def quarter_dates(quarter, year):
    ''' returns (start, end) date obj for a quarter and year '''
    if quarter == 1:
        s, e = (1, 1), (3, 31)
    if quarter == 2:
        s, e = (4, 1), (6, 30)
    if quarter == 3:
        s, e = (7, 1), (9, 30)
    if quarter == 4:
        s, e = (10, 1), (12, 31)

    return (date(year, *s), date(year, *e))


def check_periods(date_ref):
    ''' ensure existence of current, previous and next period for a date '''
    pass