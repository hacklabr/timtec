# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('core', '0015_auto_20160406_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='groups',
            field=models.ManyToManyField(help_text='The Groups that can have access to this forum. If empty, there are no group restrictions.', related_name='courses', verbose_name='groups', to='auth.Group', blank=True),
        ),
        migrations.AddField(
            model_name='class',
            name='user_can_certificate_even_without_progress',
            field=models.BooleanField(default=False, verbose_name='Certification Allowed Even Without Progress'),
        ),
    ]
