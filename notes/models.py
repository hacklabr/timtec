# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Note(models.Model):
    text = models.TextField(_('Note'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    create_timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    last_edit_timestamp = models.DateTimeField(auto_now=True, editable=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
