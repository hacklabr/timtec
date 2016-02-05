# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_coursecertification_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='klass',
            field=models.ForeignKey(related_name='evaluations', verbose_name='Class', to='core.Class'),
        ),
    ]
