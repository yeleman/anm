#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date, datetime

from gettext import gettext as _
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Table, Column, Integer, String, \
                       MetaData, ForeignKey, Date, DateTime, Unicode

DB_FILE = 'anm.db'

engine = create_engine('sqlite:///%s' % DB_FILE, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

metadata = MetaData()

periods_table = Table('period', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
    Column('start_on', Date, unique=True),
    Column('end_on', Date, unique=True),
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
    Column('invoice_date', Date),
    Column('provider', Unicode(100)),
    Column('amount', Integer),
    Column('registered_on', Date, nullable=True),
)

revisions_table = Table('revision', metadata,
    Column('id', Integer, primary_key=True),
    Column('num', Integer, unique=True),
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

    def display_name(self):
        suffixes = {1: _(u"st"), 2: _(u"nd"), 3: _("rd"), 4: _("th")}
        return _(u"%(quar)d%(suf)s Quarter %(year)s") \
               % {'quar': self.quarter, 'suf': suffixes[self.quarter], \
                  'year': self.year}

    @property
    def year(self):
        return self.start_on.year

    @property
    def quarter(self):
        from data_helpers import quarter_for

        return quarter_for(self.start_on)

    def auto_name(self):
        return _(u"Q%(quarter)d %(year)d") \
               % {'quarter': self.quarter, 'year': self.year}

    def short_name(self):
        return _(u"Q%(quarter)d/%(year)d") \
               % {'quarter': self.quarter, 'year': self.year}

    def next(self):
        from data_helpers import next_quarter, quarter_dates, period_for
        ns, ne = quarter_dates(*next_quarter(self.quarter, self.year))
        return period_for(ns)

    def previous(self):
        from data_helpers import previous_quarter, quarter_dates, period_for
        ns, ne = quarter_dates(*previous_quarter(self.quarter, self.year))
        return period_for(ns)


class Account(object):
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __repr__(self):
        return "<Account('%s')>" % (self.number)

    def __unicode__(self):
        return _(u"%s") % self.name


class Budget(object):
    def __init__(self, amount, account=None, period=None):
        self.amount = amount
        self.account = account
        self.period = period

    def __repr__(self):
        return "<Budget('%s','%s')>" % (self.period, self.amount)

    def __unicode__(self):
        return _(u"%(account)s %(period)s: %(amount)s") \
               % {'account': self.account.number, \
                  'period': self.period.short_name(), 'amount': self.amount}


class Operation(object):
    def __init__(self, order_number, invoice_number, \
                 invoice_date, provider, amount, \
                 registered_on=datetime.now(), account=None):
        self.order_number = order_number
        self.invoice_number = invoice_number
        self.invoice_date = invoice_date
        self.provider = provider
        self.amount = amount
        self.registered_on = registered_on
        self.account = account

    def __repr__(self):
        return "<Operation('%s','%s')>" % (self.account, self.amount)

    def __unicode__(self):
        return _(u"%(inv_num)s %(inv_date)s: %(amount)s") \
               % {'inv_num': self.invoice_number, \
                  'inv_date': self.invoice_date.strftime('%F'), \
                  'amount': self.amount}

    def period(self):
        return session.query(Period).filter_by()


class Revision(object):
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return "<Revision('%d')>" % self.num

    def __unicode__(self):
        return u"%s" % self.__repr__()

mapper(Account, accounts_table, properties={
    'operations': relationship(Operation, backref='account'),
    'budgets': relationship(Budget, backref='account'),
})
mapper(Period, periods_table, properties={
    'budgets': relationship(Budget, backref='period'),
})
mapper(Budget, budgets_table)
mapper(Operation, operations_table)
mapper(Revision, revisions_table)
