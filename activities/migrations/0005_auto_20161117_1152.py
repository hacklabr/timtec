# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20160817_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='activity',
            field=models.ForeignKey(related_name='answers', verbose_name='Activity', to='activities.Activity'),
        ),
    ]
