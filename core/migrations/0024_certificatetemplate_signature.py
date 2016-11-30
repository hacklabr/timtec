# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_remove_class_assistant'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificatetemplate',
            name='signature',
            field=models.ImageField(upload_to=core.utils.HashName(b'signature', b'organization_name'), null=True, verbose_name='Signature', blank=True),
        ),
    ]
