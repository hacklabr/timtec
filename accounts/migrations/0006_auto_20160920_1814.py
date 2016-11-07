# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160920_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersocialaccount',
            name='social_media',
            field=models.CharField(max_length=15, verbose_name='social media', choices=[(b'facebook', 'Facebook'), (b'instagram', 'Instagram'), (b'snapchat', 'Snapchat'), (b'whatsapp', 'Whatsapp'), (b'twitter', 'Twitter'), (b'linkedin', 'Linked-In'), (b'youtube', 'Youtube')]),
        ),
    ]
