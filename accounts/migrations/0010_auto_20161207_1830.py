# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20160928_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timtecuser',
            name='state',
            field=models.CharField(max_length=30, verbose_name='Province', blank=True),
        ),
    ]
