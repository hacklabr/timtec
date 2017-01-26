# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0019_auto_20161014_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='professormessage',
            name='users_that_read',
            field=models.ManyToManyField(related_name='read_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
