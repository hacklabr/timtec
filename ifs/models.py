# coding=utf-8
from django.db import models
from accounts.models import AbstractTimtecUser
from django.utils.translation import ugettext_lazy as _


class IfUser(AbstractTimtecUser):
    # students fields
    # if_id eh o identificador de matricula
    ifid = models.CharField(_('Academic ID'), max_length=30, blank=True)
    course = models.CharField(_('Course'), max_length=30, blank=True)
    klass = models.CharField(_('Class'), max_length=30, blank=True)

    # professors fields
    cpf = models.CharField(_('Cpf'), max_length=30, blank=True)
    siape = models.CharField(_('Siape'), max_length=30, blank=True)

    # common fields
    campus = models.CharField(_('Campus'), max_length=30, blank=True)
    is_if_staff = models.BooleanField(default=False)

    class Meta(AbstractTimtecUser.Meta):
        swappable = 'AUTH_USER_MODEL'
