# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151104_0157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursecertification',
            name='course',
        ),
        migrations.AlterField(
            model_name='certificationprocess',
            name='comments',
            field=models.CharField(max_length=255, null=True, verbose_name='Comments', blank=True),
        ),
    ]
