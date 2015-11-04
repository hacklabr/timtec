# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151003_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecertification',
            name='course',
            field=models.ForeignKey(default=10, verbose_name='Course', to='core.Course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursecertification',
            name='course_student',
            field=models.OneToOneField(related_name='certificate', verbose_name='Enrollment', to='core.CourseStudent'),
        ),
    ]
