# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_coursecertification_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificationprocess',
            name='evaluation',
            field=models.ForeignKey(related_name='processes', verbose_name='Evaluation', blank=True, to='core.Evaluation', null=True),
        ),
        migrations.AlterField(
            model_name='certificationprocess',
            name='evaluation_grade',
            field=models.IntegerField(null=True, verbose_name='Evaluation grade', blank=True),
        ),
    ]
