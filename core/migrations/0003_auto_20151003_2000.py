# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20150904_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Certificate Template',
            },
        ),
        migrations.AddField(
            model_name='certificationprocess',
            name='klass',
            field=models.ForeignKey(related_name='processes', default=1, verbose_name='Class', to='core.Class'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='certificationprocess',
            name='student',
            field=models.ForeignKey(related_name='processes', default=1, verbose_name='Student', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='user_can_certificate',
            field=models.BooleanField(default=False, verbose_name='Certification Allowed'),
        ),
        migrations.AlterField(
            model_name='certificationprocess',
            name='course_certification',
            field=models.ForeignKey(verbose_name='Certificate', to='core.CourseCertification', null=True),
        ),
        migrations.AlterField(
            model_name='certificationprocess',
            name='evaluation',
            field=models.ForeignKey(related_name='processes', verbose_name='Evaluation', to='core.Evaluation', null=True),
        ),
        migrations.CreateModel(
            name='IfCertificateTemplate',
            fields=[
                ('certificatetemplate_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.CertificateTemplate')),
                ('pronatec_logo', models.BooleanField(default=False, verbose_name='Pronatec')),
                ('mec_logo', models.BooleanField(default=True, verbose_name='MEC')),
                ('logo', models.ImageField(upload_to=core.utils.HashName(b'if_logo', b'if_name'), null=True, verbose_name='Logo', blank=True)),
                ('if_name', models.CharField(max_length=30, null=True, verbose_name='Name', blank=True)),
                ('signature', models.ImageField(upload_to=core.utils.HashName(b'if_signature', b'if_name'), null=True, verbose_name='Signature', blank=True)),
                ('signature_name', models.CharField(max_length=255, null=True, verbose_name='Signature Name', blank=True)),
            ],
            options={
                'verbose_name': 'IF Certificate Template',
            },
            bases=('core.certificatetemplate',),
        ),
        migrations.AddField(
            model_name='certificatetemplate',
            name='course',
            field=models.OneToOneField(verbose_name='Course', to='core.Course'),
        ),
    ]
