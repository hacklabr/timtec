# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20160406_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='user_can_certificate_even_without_progress',
            field=models.BooleanField(default=False, verbose_name='Certification Allowed Even Without Progress'),
        ),
    ]
