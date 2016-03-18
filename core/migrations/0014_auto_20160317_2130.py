# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20160315_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificatetemplate',
            name='organization_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Name', blank=True),
        ),
    ]
