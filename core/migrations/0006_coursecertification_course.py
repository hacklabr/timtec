# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20151104_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecertification',
            name='course',
            field=models.ForeignKey(default=1, verbose_name='Course', to='core.Course'),
            preserve_default=False,
        ),
    ]
