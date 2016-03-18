# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.utils
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160131_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ifcertificatetemplate',
            name='if_name',
        ),
        migrations.RemoveField(
            model_name='ifcertificatetemplate',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='ifcertificatetemplate',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='ifcertificatetemplate',
            name='signature_name',
        ),
        migrations.AddField(
            model_name='certificatetemplate',
            name='base_logo',
            field=models.ImageField(upload_to=core.utils.HashName(b'base_logo', b'organization_name'), null=True, verbose_name='Logo', blank=True),
        ),
        migrations.AddField(
            model_name='certificatetemplate',
            name='cert_logo',
            field=models.ImageField(upload_to=core.utils.HashName(b'logo', b'organization_name'), null=True, verbose_name='Logo', blank=True),
        ),
        migrations.AddField(
            model_name='certificatetemplate',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Signature Name', blank=True),
        ),
        migrations.AddField(
            model_name='certificatetemplate',
            name='organization_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Name', blank=True),
        ),
        migrations.AddField(
            model_name='certificatetemplate',
            name='role',
            field=models.CharField(max_length=128, null=True, verbose_name='Role', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=128, unique=True, verbose_name='Slug'),
        ),
    ]
