# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20170120_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professormessageread',
            name='message',
            field=models.ForeignKey(related_name='read_status', verbose_name='ProfessorMessage', to='core.ProfessorMessage'),
        ),
    ]
