# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='Answer')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Question')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'title', unique=True, verbose_name='Slug')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('hidden_justification', models.TextField(default=None, null=True, verbose_name='Justification', blank=True)),
                ('correct_answer', models.OneToOneField(related_name='+', null=True, blank=True, to='forum.Answer', verbose_name='Correct answer')),
                ('course', models.ForeignKey(verbose_name='Course', to='core.Course')),
                ('hidden_by', models.ForeignKey(related_name='hidden_questions', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='User')),
                ('lesson', models.ForeignKey(related_name='forum_questions', verbose_name='Lesson', blank=True, to='core.Lesson', null=True)),
                ('user', models.ForeignKey(related_name='forum_questions', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('vote_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='forum.Vote')),
            ],
            bases=('forum.vote',),
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('vote_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='forum.Vote')),
                ('question', models.ForeignKey(related_name='votes', verbose_name='Question', to='forum.Question')),
            ],
            bases=('forum.vote',),
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', verbose_name='Question', to='forum.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(related_name='forum_answers', verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answervote',
            name='answer',
            field=models.ForeignKey(related_name='votes', verbose_name='Answer', to='forum.Answer'),
        ),
    ]
