# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20160923_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='timtecuser',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Birth Date', blank=True),
        ),
    ]
