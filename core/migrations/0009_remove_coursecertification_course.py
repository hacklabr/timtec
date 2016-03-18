# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151203_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursecertification',
            name='course',
        ),
    ]
