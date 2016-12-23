# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from core.models import Course, Lesson
from django.conf import settings


class Question(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    text = models.TextField(_('Question'))
    slug = AutoSlugField(_('Slug'), populate_from='title', max_length=255, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='forum_questions')
    correct_answer = models.OneToOneField('Answer', verbose_name=_('Correct answer'), related_name='+', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    course = models.ForeignKey(Course, verbose_name=_('Course'))
    lesson = models.ForeignKey(Lesson, verbose_name=_('Lesson'), related_name='forum_questions', null=True, blank=True)
    hidden = models.BooleanField(verbose_name=_('Hidden'), default=False)
    hidden_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='hidden_questions', default=None, null=True, blank=True)
    hidden_justification = models.TextField(_('Justification'), default=None, null=True, blank=True)

    def save(self, **kwargs):
        if not self.id and self.title:
            self.slug = slugify(self.title)
        super(Question, self).save(**kwargs)

    def __unicode__(self):
        return self.title

    @property
    def count_votes(self):
        return self.votes.aggregate(models.Sum('value'))['value__sum'] or 0

    @property
    def likes(self):
        return self.votes.aggregate(
            total=models.Count(
                models.Case(
                    models.When(value__gt=0, then=1),
                    output_field=models.CharField(),
                )
            ))['total']

    @property
    def unlikes(self):
        return self.votes.aggregate(
            total=models.Count(
                models.Case(
                    models.When(value__lt=0, then=1),
                    output_field=models.CharField(),
                )
            ))['total']


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', verbose_name=_('Question'))
    text = models.TextField(_('Answer'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='forum_answers')
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.text

    @property
    def count_votes(self):
        return self.votes.aggregate(models.Sum('value'))['value__sum'] or 0


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    timestamp = models.DateTimeField(auto_now=True)
    # Defines vote up or vote down. Vote up:1; Vote down: -1.
    value = models.IntegerField(null=False, blank=False, default=0)


class QuestionVote(Vote):
    question = models.ForeignKey(Question, related_name='votes', verbose_name=_('Question'))

#     class Meta:
#         unique_together = ('question', 'user')


class AnswerVote(Vote):
    answer = models.ForeignKey(Answer, related_name='votes', verbose_name=_('Answer'))

#     class Meta:
#         unique_together = ('answer', 'user')
