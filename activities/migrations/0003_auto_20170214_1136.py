# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20160923_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='image',
            field=models.ImageField(upload_to=b'activities', null=True, verbose_name='Image', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='comment',
            field=models.TextField(null=True, verbose_name='Comment', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='data',
            field=jsonfield.fields.JSONField(null=True, verbose_name='Data', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='expected',
            field=jsonfield.fields.JSONField(null=True, verbose_name='Expected answer', blank=True),
        ),
    ]
