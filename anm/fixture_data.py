#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date, datetime

from sqlalchemy import desc

from database import *
from data_helpers import period_for


def initial_setup():

    DB_REVISION = 1

    try:
        revision = session.query(Revision.num)\
                          .order_by(desc(Revision.num)).scalar()
    except:
        revision = 0

    if revision >= DB_REVISION:
        return

    period = period_for(date(2011, 1, 1))

    data = [
        ('2-611-00', u"Personnel", 938882000),
        ('2-613-23', u"Indemnité de session", 0),
        ('3-621-10', u"Dépenses Matériel-fonctionnement des services", \
                                                                    227325000),
        ('3-621-20', u"Besoins nouveaux des Services", 44100000),
        ('3-622-30', u"Entretien des bâtiments", 26265000),
        ('3-623-10', u"Honoraires et frais d'étude administrative", 0),
        ('3-625-10', u"Électricité et eau", 59678000),
        ('3-626-10', u"Redevances téléphoniques", 56403000),
        ('3-626-20', u"Frais postaux", 1128000),
        ('3-628-10', u"Indemnité de déplacement", 302565000),
        ('3-628-20', u"Frais de transport", 479251000),
        ('3-629-76', u"Autres dépenses de matériel", 20371000),
        ('4-641-36', u"Appui PAGAMGFP (CF/AN)", 0),
        ('4-643-10', u"Participation au fonctionnement", 263400000),
        ('4-645-20', u"Contribution du fonct. des organismes", 18652000),
        ('5-234-10', u"Dépenses en Investissement", 0),
    ]

    r = Revision(DB_REVISION)
    session.add(r)

    import_account_budget_data(data, first_period=period)


def import_account_budget_data(data, first_period):

    # create list of periods based on number of elements
    # in data's first tuple.
    periods = []
    for index in xrange(0, len(data[0][-(len(data[0]) - 2):])):
        if index == 0:
            period = first_period
        else:
            period = periods[-1].next()
        periods.append(period)

    for row in data:
        a = Account(number=row[0], name=row[1])
        session.add(a)
        for index, period in enumerate(periods):
            b = Budget(amount=row[2 + index], period=period, account=a)
            session.add(b)
    session.commit()


def period_check(date_ref):
    # check current period and perdiod + 1 exist
    pass
