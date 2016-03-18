# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20160131_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
