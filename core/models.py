# -*- coding: utf-8 -*-
import re
import json

from jsonfield import JSONField
from positions import PositionField

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.staticfiles.storage import staticfiles_storage
from allauth.account.signals import user_signed_up

import os
import hashlib


def path_and_rename(path):
    def wrapper(instance, filename):
        root, ext = os.path.splitext(filename)
        m = hashlib.md5()
        m.update(root.encode('utf-8'))
        m.update(instance.username.encode('utf-8'))
        filename = m.hexdigest() + ext
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper


class TimtecUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_REGEXP = re.compile('^[\w.+-]+$')
    username = models.CharField(
        _('Username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    './+/-/_ characters'),
        validators=[
            validators.RegexValidator(USERNAME_REGEXP, _('Enter a valid username.'), 'invalid')
        ])

    email = models.EmailField(_('Email address'), blank=False, unique=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    picture = models.ImageField(_("Picture"), upload_to=path_and_rename('user-pictures'), blank=True)
    occupation = models.CharField(_('Occupation'), max_length=30, blank=True)
    city = models.CharField(_('City'), max_length=30, blank=True)
    site = models.URLField(_('Site'), blank=True)
    biography = models.TextField(_('Biography'), blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.email

    def get_picture_url(self):
        if not self.picture:
            location = "/%s/%s" % (settings.STATIC_URL, 'img/avatar-default.png')
        else:
            location = "/%s/%s" % (settings.MEDIA_URL, self.picture)
        return re.sub('/+', '/', location)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def get_user_type(self):
        if self.is_superuser:
            return "superuser"
        elif self.groups.filter(name='professors').count():
            return "professors"
        elif self.groups.filter(name='students').count():
            return "students"
        return "unidentified"

    def is_pilot(self):
        return self.groups.filter(name='pilot_course').count() > 0

    @staticmethod
    def add_default_group(sender, user, **kwargs):
        if settings.REGISTRATION_DEFAULT_GROUP_NAME:
            user.groups.add(Group.objects.get(name=settings.REGISTRATION_DEFAULT_GROUP_NAME))
            user.save()

user_signed_up.connect(TimtecUser.add_default_group, dispatch_uid="TimtecUser.add_default_group")


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
        ('draft', _('Draft')),
        ('listed', _('Listed')),
        ('published', _('Published')),
    )

    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    name = models.CharField(_('Name'), max_length=255)
    intro_video = models.ForeignKey(Video, verbose_name=_('Intro video'), null=True)
    application = models.TextField(_('Application'))
    requirement = models.TextField(_('Requirement'))
    abstract = models.TextField(_('Abstract'))
    structure = models.TextField(_('Structure'))
    workload = models.TextField(_('Workload'))
    pronatec = models.TextField(_('Pronatec'))
    status = models.CharField(_('Status'), choices=STATES, default=STATES[0][0], max_length=64)
    publication = models.DateField(_('Publication'), )
    professors = models.ManyToManyField(TimtecUser, related_name='professorcourse_set', through='CourseProfessor')
    students = models.ManyToManyField(TimtecUser, related_name='studentcourse_set', through='CourseStudent')

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __unicode__(self):
        return self.name

    @property
    def unit_set(self):
        return Unit.objects.filter(lesson__in=self.lesson_set.all()).order_by('lesson')

    @property
    def public_lessons(self):
        return self.lesson_set.exclude(status='draft')

    def first_lesson(self):
        if self.lesson_set.exists():
            return self.lesson_set.all()[0]

    def enroll_student(self, student):
        params = {'user': student, 'course': self}
        try:
            return CourseStudent.objects.get(**params)
        except CourseStudent.DoesNotExist:
            return CourseStudent.objects.create(**params)


class CourseStudent(models.Model):
    user = models.ForeignKey(TimtecUser, verbose_name=_('Student'))
    course = models.ForeignKey(Course, verbose_name=_('Course'))

    class Meta:
        unique_together = (('user', 'course'),)

    @property
    def units_done(self):
        return StudentProgress.objects.exclude(complete=None)\
                                      .filter(user=self.user, unit__lesson__course=self.course)

    def resume_last_unit(self):
        units_done = self.units_done.order_by('complete')
        # import ipdb; ipdb.set_trace()
        if units_done.count() > 0:
            return units_done.reverse().first().unit
        else:
            try:
                return self.course.first_lesson().units.order_by('position').first()
            except (AttributeError):
                return None

    def percent_progress(self):
        units_len = self.course.unit_set.count()
        units_done_len = self.units_done.count()
        return int(100.0 * units_done_len / units_len)


class CourseProfessor(models.Model):
    ROLES = (
        ('instructor', _('Instructor')),
        ('assistant', _('Assistant')),
        ('pedagogy_assistant', _('Pedagogy Assistant')),
    )

    user = models.ForeignKey(TimtecUser, verbose_name=_('Professor'))
    course = models.ForeignKey(Course, verbose_name=_('Course'))
    biography = models.TextField(_('Biography'))
    role = models.CharField(_('Role'), choices=ROLES, default=ROLES[0][0], max_length=128)

    class Meta:
        unique_together = (('user', 'course'),)
        verbose_name = _('Course Professor')
        verbose_name_plural = _('Course Professors')

    def __unicode__(self):
        return u'%s @ %s' % (self.user, self.course)


class Lesson(models.Model):
    STATES = (
        ('draft', _('Draft')),
        ('listed', _('Listed')),
        ('published', _('Published')),
    )

    course = models.ForeignKey(Course, verbose_name=_('Course'))
    desc = models.CharField(_('Description'), max_length=255)
    name = models.CharField(_('Name'), max_length=255)
    notes = models.TextField(_('Notes'), default="", blank=True)
    position = PositionField(collection='course', default=0)
    slug = models.SlugField(_('Slug'), max_length=255, editable=False, unique=True)
    status = models.CharField(_('Status'), choices=STATES, default=STATES[0][0], max_length=64)

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

    def thumbnail(self):
        try:
            first_vid_unit = self.units.exclude(video=None).order_by('position')[0]
            thumbnail = 'http://i1.ytimg.com/vi/' + first_vid_unit.video.youtube_id + '/hqdefault.jpg'
            return thumbnail
        except IndexError:
            return staticfiles_storage.url('img/lesson-default.png')

    def activity_count(self):
        return self.units.exclude(activity=None).count()

    def unit_count(self):
        return self.units.all().count()

    def video_count(self):
        return self.units.exclude(video=None).count()

    def is_ready(self):
        return self.status == 'published' and self.units.exists()


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
    expected = JSONField(_('Expected answer'))

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __unicode__(self):
        return u'%s dt %s a %s' % (self.type, self.data, self.expected)


class Unit(models.Model):
    title = models.CharField(_('Title'), max_length=128, blank=True)
    lesson = models.ForeignKey(Lesson, verbose_name=_('Lesson'), related_name='units')
    video = models.ForeignKey(Video, verbose_name=_('Video'), null=True, blank=True)
    activity = models.ForeignKey(Activity, verbose_name=_('Activity'), null=True, blank=True)
    position = PositionField(collection='lesson', default=0)

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ['lesson', 'position']

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.lesson, self.position, self.video, self.activity)

    @staticmethod
    def set_position_for_new_unit(sender, instance, **kwargs):
        if instance.id:
            return

        latest = sender.objects.filter(lesson=instance.lesson) \
                               .aggregate(models.Max('position')) \
                               .get('position__max')

        if latest is not None:
            instance.position = latest + 1


models.signals.pre_save.connect(Unit.set_position_for_new_unit, sender=Unit,
                                dispatch_uid="Unit.set_position_for_new_unit")


class Answer(models.Model):
    activity = models.ForeignKey(Activity, verbose_name=_('Activity'))
    user = models.ForeignKey(TimtecUser, verbose_name=_('Student'))
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    given = JSONField(_('Given answer'))

    @property
    def expected(self):
        if type(self.activity.expected) in [unicode, str]:
            return json.loads(self.activity.expected)
        return self.activity.expected

    def is_correct(self):
        if self.activity.type == 'html5':
            return True

        result = False

        given = self.given
        expected = self.activity.expected

        result = unicode(given) == unicode(expected)
        return result

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        ordering = ['timestamp']


class StudentProgress(models.Model):
    user = models.ForeignKey(TimtecUser, verbose_name=_('Student'))
    unit = models.ForeignKey(Unit, verbose_name=_('Unit'), related_name='progress')
    complete = models.DateTimeField(editable=True, null=True, blank=True)
    last_access = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = (('user', 'unit'),)
        verbose_name = _('Student Progress')

    def __unicode__(self):
        return u'%s @ %s c: %s la: %s' % (self.user, self.unit, self.complete, self.last_access)
