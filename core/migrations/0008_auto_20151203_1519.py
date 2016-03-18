# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151202_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificationprocess',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='certificationprocess',
            name='course_certification',
            field=models.ForeignKey(related_name='processes', verbose_name='Certificate', to='core.CourseCertification', null=True),
        ),
    ]
