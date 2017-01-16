# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_questionview'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 16, 14, 18, 10, 65461, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
