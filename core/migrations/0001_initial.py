# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.utils
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('assistant', models.ForeignKey(related_name='professor_classes', verbose_name='Assistant', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('name', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('application', models.TextField(verbose_name='Application', blank=True)),
                ('requirement', models.TextField(verbose_name='Requirement', blank=True)),
                ('abstract', models.TextField(verbose_name='Abstract', blank=True)),
                ('structure', models.TextField(verbose_name='Structure', blank=True)),
                ('workload', models.TextField(verbose_name='Workload', blank=True)),
                ('pronatec', models.TextField(verbose_name='Pronatec', blank=True)),
                ('status', models.CharField(default=b'draft', max_length=64, verbose_name='Status', choices=[(b'draft', 'Draft'), (b'published', 'Published')])),
                ('thumbnail', models.ImageField(upload_to=core.utils.HashName(b'course_thumbnails', b'name'), null=True, verbose_name='Thumbnail', blank=True)),
                ('home_thumbnail', models.ImageField(upload_to=core.utils.HashName(b'home_thumbnails', b'name'), null=True, verbose_name='Home thumbnail', blank=True)),
                ('home_position', models.IntegerField(null=True, blank=True)),
                ('start_date', models.DateField(default=None, null=True, verbose_name='Start date', blank=True)),
                ('home_published', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='CourseAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biography', models.TextField(null=True, verbose_name='Biography', blank=True)),
                ('picture', models.ImageField(upload_to=core.utils.HashName(b'bio-pictures', b'name'), null=True, verbose_name='Picture', blank=True)),
                ('name', models.TextField(max_length=30, null=True, verbose_name='Name', blank=True)),
                ('position', models.IntegerField(default=100, null=True, blank=True)),
                ('course', models.ForeignKey(related_name='course_authors', verbose_name='Course', to='core.Course')),
                ('user', models.ForeignKey(related_name='authoring_courses', verbose_name='Professor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Course Author',
                'verbose_name_plural': 'Course Authors',
            },
        ),
        migrations.CreateModel(
            name='CourseProfessor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biography', models.TextField(null=True, verbose_name='Biography', blank=True)),
                ('role', models.CharField(default=b'assistant', max_length=128, verbose_name='Role', choices=[(b'instructor', 'Instructor'), (b'assistant', 'Assistant'), (b'coordinator', 'Professor Coordinator')])),
                ('picture', models.ImageField(upload_to=core.utils.HashName(b'bio-pictures', b'name'), null=True, verbose_name='Picture', blank=True)),
                ('name', models.TextField(max_length=30, null=True, verbose_name='Name', blank=True)),
                ('is_course_author', models.BooleanField(default=False)),
                ('course', models.ForeignKey(related_name='course_professors', verbose_name='Course', to='core.Course')),
                ('user', models.ForeignKey(related_name='teaching_courses', verbose_name='Professor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Course Professor',
                'verbose_name_plural': 'Course Professors',
            },
        ),
        migrations.CreateModel(
            name='CourseStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(verbose_name='Course', to='core.Course')),
                ('user', models.ForeignKey(verbose_name='Student', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['course__start_date'],
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('subject', models.CharField(max_length=255)),
                ('template', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.TextField(verbose_name='Description')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('notes', models.TextField(default=b'', verbose_name='Notes', blank=True)),
                ('position', models.IntegerField(default=0)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', max_length=255, unique=True, verbose_name='Slug')),
                ('status', models.CharField(default=b'draft', max_length=64, verbose_name='Status', choices=[(b'draft', 'Draft'), (b'published', 'Published')])),
                ('course', models.ForeignKey(related_name='lessons', verbose_name='Course', to='core.Course')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='ProfessorMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255, verbose_name='Subject')),
                ('message', models.TextField(verbose_name='Message')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('course', models.ForeignKey(verbose_name='Course', to='core.Course', null=True)),
                ('professor', models.ForeignKey(verbose_name='Professor', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complete', models.DateTimeField(null=True, blank=True)),
                ('last_access', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Student Progress',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title', blank=True)),
                ('side_notes', models.TextField(verbose_name='Side notes', blank=True)),
                ('position', models.IntegerField(default=0)),
                ('lesson', models.ForeignKey(related_name='units', verbose_name='Lesson', to='core.Lesson')),
            ],
            options={
                'ordering': ['lesson', 'position'],
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('youtube_id', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
        migrations.AddField(
            model_name='unit',
            name='video',
            field=models.ForeignKey(related_name='unit', verbose_name='Video', blank=True, to='core.Video', null=True),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='unit',
            field=models.ForeignKey(related_name='progress', verbose_name='Unit', to='core.Unit'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='user',
            field=models.ForeignKey(verbose_name='Student', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='authors',
            field=models.ManyToManyField(related_name='authorcourses', through='core.CourseAuthor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='default_class',
            field=models.OneToOneField(related_name='default_course', null=True, blank=True, to='core.Class', verbose_name='Default Class'),
        ),
        migrations.AddField(
            model_name='course',
            name='intro_video',
            field=models.ForeignKey(verbose_name='Intro video', blank=True, to='core.Video', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='professors',
            field=models.ManyToManyField(related_name='professorcourse_set', through='core.CourseProfessor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='studentcourse_set', through='core.CourseStudent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(verbose_name='Course', to='core.Course'),
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(related_name='classes', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='studentprogress',
            unique_together=set([('user', 'unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursestudent',
            unique_together=set([('user', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseprofessor',
            unique_together=set([('user', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseauthor',
            unique_together=set([('user', 'course')]),
        ),
    ]
