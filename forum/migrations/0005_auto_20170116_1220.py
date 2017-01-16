# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0004_questionview_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionVisualization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(related_name='views', verbose_name='Question', to='forum.Question')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='questionview',
            name='question',
        ),
        migrations.RemoveField(
            model_name='questionview',
            name='user',
        ),
        migrations.DeleteModel(
            name='QuestionView',
        ),
    ]
