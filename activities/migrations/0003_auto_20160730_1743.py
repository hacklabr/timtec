# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_activity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='data',
            field=jsonfield.fields.JSONField(verbose_name='Data', blank=True),
        ),
    ]
