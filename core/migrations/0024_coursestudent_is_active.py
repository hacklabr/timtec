# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_coursestudent_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursestudent',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active?'),
        ),
    ]
