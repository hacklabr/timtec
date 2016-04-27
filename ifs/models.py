# coding=utf-8
from django.db import models
from accounts.models import AbstractTimtecUser
from django.utils.translation import ugettext_lazy as _


class Campus(models.Model):
    name = models.CharField(_('Name'), max_length=30, blank=True)
    city = models.CharField(_('City'), max_length=30)
    address = models.CharField(_('Address'), max_length=30, blank=True)

    def __unicode__(self):
        return self.name or self.city


class IfUser(AbstractTimtecUser):
    # students fields
    # if_id eh o identificador de matricula
    email = models.EmailField(_('Email address'), blank=True, unique=False)

    ifid = models.CharField(_('Academic ID'), max_length=30, blank=True)
    course = models.CharField(_('Course'), max_length=30, blank=True)
    klass = models.CharField(_('Class'), max_length=30, blank=True)

    # professors fields
    cpf = models.CharField(_('Cpf'), max_length=30, blank=True)
    siape = models.CharField(_('Siape'), max_length=30, blank=True)

    # common fields
    campus = models.ForeignKey(Campus, verbose_name=_('Campus'), related_name='users', null=True, blank=True)
    is_if_staff = models.BooleanField(default=False)
