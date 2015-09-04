# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificationProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comments', models.CharField(max_length=255, verbose_name='Comments')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('evaluation_grade', models.IntegerField(verbose_name='Evaluation grade', blank=True)),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('no_show', models.BooleanField(default=False, verbose_name='No show')),
            ],
            options={
                'verbose_name': 'Certification Process',
            },
        ),
        migrations.CreateModel(
            name='CourseCertification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=127, verbose_name='Certificate Type', choices=[(b'receipt', 'Receipt'), (b'certificate', 'Certificate')])),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('is_valid', models.BooleanField(default=False, verbose_name='Certificate is valid')),
                ('course_workload', models.TextField(verbose_name='Workload', blank=True)),
                ('course_total_units', models.IntegerField(verbose_name='Total units', blank=True)),
                ('link_hash', models.CharField(max_length=255, verbose_name='Hash')),
                ('course_student', models.OneToOneField(verbose_name='Enrollment', to='core.CourseStudent')),
            ],
            options={
                'verbose_name': 'Certificate',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('min_grade', models.IntegerField(verbose_name='Evaluation grade needed', blank=True)),
                ('date', models.DateTimeField(verbose_name='Evaluation date', blank=True)),
                ('results_date', models.DateTimeField(verbose_name='Evaluation results date', blank=True)),
                ('instructions', models.CharField(max_length=255, verbose_name='Comments')),
                ('klass', models.ForeignKey(verbose_name='Class', to='core.Class')),
            ],
            options={
                'verbose_name': 'Evaluation',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='min_percent_to_complete',
            field=models.IntegerField(default=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='certificationprocess',
            name='course_certification',
            field=models.ForeignKey(verbose_name='Certificate', to='core.CourseCertification'),
        ),
        migrations.AddField(
            model_name='certificationprocess',
            name='evaluation',
            field=models.ForeignKey(verbose_name='Evaluation', to='core.Evaluation'),
        ),
    ]
