# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_timtecuser_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='timtecuser',
            name='how_you_know',
            field=models.CharField(max_length=50, verbose_name='How do you know the platform?', blank=True),
        ),
        migrations.AddField(
            model_name='timtecuser',
            name='how_you_know_complement',
            field=models.CharField(max_length=255, verbose_name='Complement for "How do you know the platform?"', blank=True),
        ),
    ]
