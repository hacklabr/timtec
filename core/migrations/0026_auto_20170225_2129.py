# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20170214_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professormessage',
            name='users_that_read',
            field=models.ManyToManyField(related_name='read_messages', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
