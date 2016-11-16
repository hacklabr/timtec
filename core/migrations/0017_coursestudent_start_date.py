# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_course_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursestudent',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
