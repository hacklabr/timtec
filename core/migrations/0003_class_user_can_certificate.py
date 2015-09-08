# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150904_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='user_can_certificate',
            field=models.BooleanField(default=False, verbose_name='Certification Allowed'),
        ),
    ]
