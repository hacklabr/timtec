# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=255, unique=True, verbose_name='Slug'),
        ),
    ]
