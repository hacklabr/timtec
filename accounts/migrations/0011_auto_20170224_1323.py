# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20161207_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timtecuser',
            name='city',
            field=models.CharField(max_length=128, verbose_name='City', blank=True),
        ),
        migrations.AlterField(
            model_name='timtecuser',
            name='first_name',
            field=models.CharField(max_length=64, verbose_name='First name', blank=True),
        ),
        migrations.AlterField(
            model_name='timtecuser',
            name='last_name',
            field=models.CharField(max_length=128, verbose_name='Last name', blank=True),
        ),
        migrations.AlterField(
            model_name='timtecuser',
            name='occupation',
            field=models.CharField(max_length=128, verbose_name='Occupation', blank=True),
        ),
    ]
