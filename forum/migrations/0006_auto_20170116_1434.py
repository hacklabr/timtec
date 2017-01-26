# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0005_auto_20170116_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Hidden'),
        ),
        migrations.AddField(
            model_name='answer',
            name='hidden_by',
            field=models.ForeignKey(related_name='hidden_answers', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='User'),
        ),
    ]
