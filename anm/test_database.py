#!/usr/bin/env python
# encoding=utf-8

from datetime import datetime

from database import *

q1 = Period(u'Q1 2011', start_on=datetime(2011, 01, 01), \
            end_on=datetime(2011, 03, 31))

perso = Account('2344d', u'Personnel')
batim = Account('23ds3', u'Bâtiment')

bp = Budget(205765890)
bp.account = perso
bp.period = q1

bb = Budget(12560000)
bb.account = batim
bb.period = q1

achat = Operation('12', '201189n', datetime.today(), \
                  u'yɛlɛman s.à.r.l', 950000)
achat.account = perso

session.add_all((perso, batim, bp, bb, q1, achat))
session.commit()

all_accounts = session.query(Account).all()
