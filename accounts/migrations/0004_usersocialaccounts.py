# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_timtecuser_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSocialAccounts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('social_media', models.CharField(max_length=3, verbose_name='social media', choices=[(b'fac', 'Facebook'), (b'ins', 'Instagram'), (b'tel', 'Snapchat'), (b'wha', 'Whatsapp'), (b'twi', 'Twitter'), (b'lin', 'Linked-in'), (b'tel', 'Telegram'), (b'you', 'Youtube')])),
                ('nickname', models.CharField(max_length=30, verbose_name='nickname')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
