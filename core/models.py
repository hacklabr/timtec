# -*- coding: utf-8 -*-
from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

#
# TODO: Verficar se django-registration ficou compativel com `custom user`
#
#from django.contrib.auth.models import AbstractUser
#class TimtecUser(AbstractUser):
#    pass
from django.contrib.auth.models import User as TimtecUser


class Video(models.Model):
    name = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')


    def __unicode__(self):
        return self.name


class Course(models.Model):
    STATES = (
        ('new', _('New')),
        ('private', _('Private')),
        ('public', _('Public')),
    )

    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    name = models.CharField(_('Name'), max_length=255)
    intro_video = models.ForeignKey(Video, verbose_name=_('Intro video'))
    application = models.TextField(_('Application'))
    requirement = models.TextField(_('Requirement'))
    abstract = models.TextField(_('Abstract'))
    structure = models.TextField(_('Structure'))
    workload = models.TextField(_('Workload'))
    pronatec = models.TextField(_('Pronatec'))
    status = models.CharField(_('Status'), choices=STATES, default=STATES[0][0], max_length=128)
    publication = models.DateField(_('Publication'), )
    professors = models.ManyToManyField(TimtecUser, through='CourseProfessor')

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __unicode__(self):
        return self.name


class CourseProfessor(models.Model):
    class Meta:
        unique_together = (('user', 'course'),)
        verbose_name = _('Course Professor')
        verbose_name_plural = _('Course Professors')

    user = models.ForeignKey(TimtecUser, verbose_name=_('Professor'))
    course = models.ForeignKey(Course, verbose_name=_('Course'))
    biography = models.TextField(_('Biography'))

    def __unicode__(self):
        return u'%s @ %s' % (self.user, self.course)


class Lesson(models.Model):
    slug = models.SlugField(_('Slug'), max_length=255, editable=False, unique=True)
    name = models.CharField(_('Name'), max_length=255)
    desc = models.CharField(_('Description'), max_length=255)
    position = models.PositiveIntegerField(_('Position'))
    course = models.ForeignKey(Course, verbose_name=_('Course'))

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        ordering = ['position']

    def save(self, **kwargs):
        if not self.id and self.name:
            self.slug = slugify(self.name)
        super(Lesson, self).save(**kwargs)

    def __unicode__(self):
        return self.name


class Activity(models.Model):
    """
    Generic class to activities
    Data templates (data e type atributes):
    Multiple choice
        type: multiplechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choices: [0, 2, 5]} # list of espected choices, zero starting
    Single choice
        type: singlechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choice: 1}
    """
    type = models.CharField(_('Type'), max_length=255)
    data = JSONField(_('Data'))
    expected_answer = JSONField(_('Expected answer'))

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __unicode__(self):
        return u'%s dt %s a %s' % (self.type, self.data, self.expected_answer)


class Unit(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=_('Lesson'))
    video = models.ForeignKey(Video, verbose_name=_('Video'), null=True, blank=True)
    activity = models.ForeignKey(Activity, verbose_name=_('Activity'), null=True, blank=True)
    position = models.PositiveIntegerField(_('Position'))

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ['position']

    def __unicode__(self):
        return u'%s) %s - %s - %s' % (self.position, self.lesson, self.video, self.activity)


class Answer(models.Model):
    activity = models.ForeignKey(Activity, verbose_name=_('Activity'))
    user = models.ForeignKey(TimtecUser, verbose_name=_('Professor'))
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    answer = models.TextField(_('Answer'))

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
