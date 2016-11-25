# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20161125_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='assistant',
        ),
    ]
