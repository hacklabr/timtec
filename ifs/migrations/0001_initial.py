# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.utils
import re
import django.contrib.auth.models
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='IfUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, numbers and ./+/-/_ characters', unique=True, max_length=30, verbose_name='Username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.+-]+$'), 'Enter a valid username.', b'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='Last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined')),
                ('picture', models.ImageField(upload_to=core.utils.HashName(b'user-pictures', b'username'), verbose_name='Picture', blank=True)),
                ('occupation', models.CharField(max_length=30, verbose_name='Occupation', blank=True)),
                ('city', models.CharField(max_length=30, verbose_name='City', blank=True)),
                ('site', models.URLField(verbose_name='Site', blank=True)),
                ('biography', models.TextField(verbose_name='Biography', blank=True)),
                ('accepted_terms', models.BooleanField(default=False, verbose_name='Accepted terms and condition')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address', blank=True)),
                ('ifid', models.CharField(max_length=30, verbose_name='Academic ID', blank=True)),
                ('course', models.CharField(max_length=30, verbose_name='Course', blank=True)),
                ('klass', models.CharField(max_length=30, verbose_name='Class', blank=True)),
                ('cpf', models.CharField(max_length=30, verbose_name='Cpf', blank=True)),
                ('siape', models.CharField(max_length=30, verbose_name='Siape', blank=True)),
                ('is_if_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name', blank=True)),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('address', models.CharField(max_length=30, verbose_name='Address', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='ifuser',
            name='campus',
            field=models.ForeignKey(related_name='users', verbose_name='Campus', blank=True, to='ifs.Campus', null=True),
        ),
        migrations.AddField(
            model_name='ifuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='ifuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
