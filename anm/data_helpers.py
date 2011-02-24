#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sqlalchemy
from sqlalchemy import desc, func
from sqlalchemy.orm import exc

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

    budget = account_budget(account, period)
    balance = account_balance(account, period)

    return (account.number, account.name, budget, balance, account)
