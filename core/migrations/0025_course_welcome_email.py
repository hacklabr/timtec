# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_coursestudent_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='welcome_email',
            field=models.TextField(verbose_name='Welcome Email', blank=True),
        ),
    ]
