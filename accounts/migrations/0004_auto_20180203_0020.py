# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_timtecuser_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='timtecuser',
            name='institution',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timtecuser',
            name='occupation',
            field=models.CharField(max_length=127, verbose_name='Occupation', blank=True),
        ),
    ]
