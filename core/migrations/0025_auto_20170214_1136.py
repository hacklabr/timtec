# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0024_course_welcome_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessorMessageRead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_read', models.BooleanField(default=False)),
                ('message', models.ForeignKey(related_name='read_status', verbose_name='ProfessorMessage', to='core.ProfessorMessage')),
                ('user', models.ForeignKey(verbose_name='Student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='class',
            name='assistant',
        ),
        migrations.AddField(
            model_name='certificatetemplate',
            name='signature',
            field=models.ImageField(upload_to=core.utils.HashName(b'signature', b'organization_name'), null=True, verbose_name='Signature', blank=True),
        ),
        migrations.AddField(
            model_name='class',
            name='assistants',
            field=models.ManyToManyField(related_name='professor_classes', verbose_name='Assistants', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='chat_room',
            field=models.CharField(max_length=255, null=True, verbose_name='Chat Room', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='professormessageread',
            unique_together=set([('user', 'message')]),
        ),
    ]
