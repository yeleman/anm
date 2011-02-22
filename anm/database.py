#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Table, Column, Integer, String, \
                       MetaData, ForeignKey, DateTime, Unicode

engine = create_engine('sqlite:///anm.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

periods_table = Table('period', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
    Column('start_on', DateTime),
    Column('end_on', DateTime),
)

accounts_table = Table('account', metadata,
    Column('id', Integer, primary_key=True),
    Column('number', String(8), unique=True),
    Column('name', Unicode(100)),
)

budgets_table = Table('budget', metadata,
    Column('id', Integer, primary_key=True),
    Column('account_id', Integer, ForeignKey('account.id')),
    Column('period_id', Integer, ForeignKey('period.id')),
    Column('amount', Integer),
)

operations_table = Table('operation', metadata,
    Column('id', Integer, primary_key=True),
    Column('account_id', Integer, ForeignKey('account.id')),
    Column('order_number', String(20), unique=True),
    Column('invoice_number', String(20)),
    Column('invoice_date', DateTime),
    Column('provider', Unicode(100)),
    Column('amount', Integer),
)

metadata.create_all(engine)


class Period(object):
    def __init__(self, name, start_on, end_on):
        self.name = name
        self.start_on = start_on
        self.end_on = end_on

    def __repr__(self):
        return "<Period('%s', '%s')>" % (self.start_on, self.end_on)

    def __unicode__(self):
        return self.name


class Account(object):
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        return "<Account('%s')>" % (self.number)


class Budget(object):
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return "<Budget('%s','%s')>" % (self.period, self.amount)


class Operation(object):
    def __init__(self, order_number, invoice_number, \
                 invoice_date, provider, amount):
        self.order_number = order_number
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.provider = provider
        self.amount = amount

    def __repr__(self):
        return "<Operation('%s','%s')>" % (self.account, self.amount)

mapper(Account, accounts_table, properties={
    'operations': relationship(Operation, backref='account'),
    'budgets': relationship(Budget, backref='account'),
})
mapper(Period, periods_table, properties={
    'budgets': relationship(Budget, backref='period'),
})
mapper(Budget, budgets_table)
mapper(Operation, operations_table)
