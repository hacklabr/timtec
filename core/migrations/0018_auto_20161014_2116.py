# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20161014_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecertification',
            name='link_hash',
            field=models.CharField(unique=True, max_length=255, verbose_name='Hash'),
        ),
    ]
