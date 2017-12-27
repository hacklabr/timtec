# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20170125_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ifcertificatetemplate',
            name='certificatetemplate_ptr',
        ),
        migrations.AlterField(
            model_name='certificatetemplate',
            name='course',
            field=models.ForeignKey(verbose_name='Course', to='core.Course'),
        ),
        migrations.DeleteModel(
            name='IfCertificateTemplate',
        ),
    ]
