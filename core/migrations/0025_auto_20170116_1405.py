# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_certificatetemplate_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='chat_room',
            field=models.CharField(max_length=255, null=True, verbose_name='Chat Room', blank=True),
        ),
    ]
