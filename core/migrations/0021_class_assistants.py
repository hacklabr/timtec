# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0020_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='assistants',
            field=models.ManyToManyField(related_name='professor_classes', verbose_name='Assistants', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
