# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='negative_feedback',
            field=models.TextField(verbose_name='Negative Feedback', blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='positive_feedback',
            field=models.TextField(verbose_name='Positive Feedback', blank=True),
        ),
    ]
