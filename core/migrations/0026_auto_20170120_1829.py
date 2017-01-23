# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0025_auto_20170116_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessorMessageRead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_read', models.BooleanField(default=False)),
                ('message', models.ForeignKey(verbose_name='ProfessorMessage', to='core.ProfessorMessage')),
                ('user', models.ForeignKey(verbose_name='Student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='professormessageread',
            unique_together=set([('user', 'message')]),
        ),
    ]
