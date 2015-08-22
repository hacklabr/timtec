# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import course_material.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='Question')),
                ('course', models.OneToOneField(related_name='course_material', verbose_name='Course Materials', to='core.Course')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=course_material.models.get_upload_path)),
                ('course_material', models.ForeignKey(related_name='files', verbose_name='Files', to='course_material.CourseMaterial')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='coursematerial',
            unique_together=set([('id', 'course')]),
        ),
    ]
