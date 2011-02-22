# -*- coding: utf-8 -*-
import datetime
from django.db import models


class Periode(models.Model):
    name_p = models.CharField(max_length=30, verbose_name=("periode"))
    date_debut = models.DateField(verbose_name=("Date debut"))
    date_fin = models.DateField(verbose_name=("Date fin"))

    def __unicode__(self):
        return (u"%(name_p)s %(date_debut)s %(date_fin)s") % \
                                        {"name_p": self.name_p,
                                         "date_debut": self.date_debut,
                                         "date_fin": self.date_fin}


class Compte(models.Model):
    num_compte = models.CharField(max_length=100, \
                                  verbose_name=("Numero compte"))
    name_compte = models.CharField(max_length=100, \
                                    verbose_name="Nom du compte")
    periode = models.ForeignKey(Periode, verbose_name="Periode")
    montant = models.PositiveIntegerField(verbose_name="Montant")

    def __unicode__(self):
        return (u"%(num_compte)s %(name_compte)s %(periode)s %(montant)s")\
                                      % {"num_compte": self.num_compte,
                                        "name_compte": self.name_compte,
                                        "periode": self.periode,
                                        "montant": self.montant}


class Operation(models.Model):
    date_op = models.DateField(verbose_name=("Date de saisie"),
                                default= datetime.date.today)
    num_mandat = models.PositiveIntegerField(verbose_name="Numero du mandat")
    num_fact = models.CharField(max_length=100, \
                                        verbose_name="Numero de facture")
    name_fseur = models.CharField(max_length=100, \
                                                verbose_name="Montant TTC")
    compte = models.ForeignKey(Compte, verbose_name=("Le compte"))

    def __unicode__(self):
        return (u"%(num_mandat)s %(num_fact)s %(name_fseur)s %(compte)s")\
                                        % {"num_mandat": self.num_mandat,
                                            "num_fact": self.num_fact,\
                                            "name_fseur": self.name_fseur,
                                            "compte": self.compte}
