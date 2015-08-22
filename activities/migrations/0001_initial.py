# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255, verbose_name='Type')),
                ('data', jsonfield.fields.JSONField(verbose_name='Data')),
                ('expected', jsonfield.fields.JSONField(verbose_name='Expected answer', blank=True)),
                ('comment', models.TextField(verbose_name='Comment', blank=True)),
                ('unit', models.ForeignKey(related_name='activities', verbose_name='Unit', blank=True, to='core.Unit', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('given', jsonfield.fields.JSONField(verbose_name='Given answer')),
                ('activity', models.ForeignKey(verbose_name='Activity', to='activities.Activity')),
                ('user', models.ForeignKey(verbose_name='Student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
