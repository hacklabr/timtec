# coding=utf-8
from django.db import models
from accounts.models import TimtecUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import UserManager

class IfUser(TimtecUser):

    # students fields
    # if_id eh o identificador de matricula
    if_id = models.CharField(_('Course'), max_length=30, blank=True)
    course = models.CharField(_('Course'), max_length=30, blank=True)
    klass = models.CharField(_('Class'), max_length=30, blank=True)

    # professors fields
    cpf = models.CharField(_('Cpf'), max_length=30, blank=True)

    # common fields
    campus = models.CharField(_('Campus'), max_length=30, blank=True)
    siape = models.CharField(_('Siape'), max_length=30, blank=True)

    objects = UserManager()