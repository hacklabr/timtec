# -*- coding: utf-8 -*-
from __future__ import division

import datetime

from django.db import models
from django.db.models import Count
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Template, Context
from django.contrib.contenttypes import generic
from django.conf import settings
from autoslug import AutoSlugField


from accounts.models import TimtecUser
from notes.models import Note


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
        ('draft', _('Draft')),
        ('listed', _('Listed')),
        ('published', _('Published')),
    )

    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    name = models.CharField(_('Name'), max_length=255, blank=True)
    intro_video = models.ForeignKey(Video, verbose_name=_('Intro video'), null=True, blank=True)
    application = models.TextField(_('Application'), blank=True)
    requirement = models.TextField(_('Requirement'), blank=True)
    abstract = models.TextField(_('Abstract'), blank=True)
    structure = models.TextField(_('Structure'), blank=True)
    workload = models.TextField(_('Workload'), blank=True)
    pronatec = models.TextField(_('Pronatec'), blank=True)
    status = models.CharField(_('Status'), choices=STATES, default=STATES[0][0], max_length=64)
    publication = models.DateField(_('Publication'), default=None, blank=True, null=True)
    thumbnail = models.ImageField(_('Thumbnail'), upload_to='course_thumbnails', null=True, blank=True)
    professors = models.ManyToManyField(TimtecUser, related_name='professorcourse_set', through='CourseProfessor')
    students = models.ManyToManyField(TimtecUser, related_name='studentcourse_set', through='CourseStudent')
    home_thumbnail = models.ImageField(_('Home thumbnail'), upload_to='home_thumbnails', null=True, blank=True)
    home_position = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(_('Start date'), default=None, blank=True, null=True)
    home_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __unicode__(self):
        return self.name

    @property
    def unit_set(self):
        return Unit.objects.filter(lesson__in=self.lessons.all()).order_by('lesson')

    @property
    def public_lessons(self):
        return self.lessons.exclude(status='draft')

    def first_lesson(self):
        if self.lessons.exists():
            return self.lessons.all()[0]

    def enroll_student(self, student):
        params = {'user': student, 'course': self}
        try:
            return CourseStudent.objects.get(**params)
        except CourseStudent.DoesNotExist:
            return CourseStudent.objects.create(**params)

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''

    @property
    def has_started(self):
        if self.start_date <= datetime.date.today():
            return True
        else:
            return False

    def avg_lessons_users_progress(self):
        student_enrolled = self.coursestudent_set.all().count()
        progress_list = []
        for lesson in self.lessons.all():
            lesson_progress = {}
            lesson_progress['name'] = lesson.name
            lesson_progress['slug'] = lesson.slug
            lesson_progress['position'] = lesson.position
            units_len = lesson.unit_count()
            if units_len:
                units_done_len = StudentProgress.objects.exclude(complete=None).filter(unit__lesson=lesson).count()
                lesson_progress['progress'] = 100 * units_done_len / (units_len * student_enrolled)
                lesson_progress['forum_questions'] = lesson.forum_questions.count()
                # lesson_progress['progress'] =
                # lesson_progress['finish'] = self.get_lesson_finish_time(lesson)
            else:
                lesson_progress['progress'] = 0
                # lesson_progress['finish'] = ''
            progress_list.append(lesson_progress)
        return progress_list

    def forum_answers_by_lesson(self):
        return self.user.forum_answers.values('question__lesson').annotate(Count('question__lesson'))


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
        if units_done.count() > 0:
            return units_done.reverse().first().unit
        else:
            try:
                return self.course.first_lesson().units.order_by('position').first()
            except AttributeError:
                return None

    def percent_progress(self):
        units_len = self.course.unit_set.count()
        if units_len <= 0:
            return 0
        units_done_len = self.units_done.count()
        return int(100.0 * units_done_len / units_len)

    def units_done_by_lesson(self, lesson):
        return StudentProgress.objects.exclude(complete=None)\
                                      .filter(user=self.user, unit__lesson=lesson)

    def get_lesson_finish_time(self, lesson):
        latest = StudentProgress.objects.exclude(complete=None).filter(user=self.user, unit__lesson=lesson).order_by('complete')
        if latest:
            return latest.latest('complete').complete
        else:
            return ''

    def percent_progress_by_lesson(self):
        """
        Returns a list with dictionaries with keys name (lesson name), slug (lesson slug) and progress (percent lesson progress, decimal)
        """
        progress_list = []
        for lesson in self.course.lessons.all():
            lesson_progress = {}
            lesson_progress['name'] = lesson.name
            lesson_progress['slug'] = lesson.slug
            lesson_progress['position'] = lesson.position
            units_len = lesson.unit_count()
            if units_len:
                units_done_len = self.units_done_by_lesson(lesson).count()
                lesson_progress['progress'] = 100 * units_done_len / units_len
                lesson_progress['finish'] = self.get_lesson_finish_time(lesson)
            else:
                lesson_progress['progress'] = 0
                lesson_progress['finish'] = ''
            progress_list.append(lesson_progress)
        return progress_list

    def forum_questions_by_lesson(self):
        return self.user.forum_questions.values('lesson').annotate(Count('lesson'))

    def forum_answers_by_lesson(self):
        return self.user.forum_answers.values('question__lesson').annotate(Count('question__lesson'))


class CourseProfessor(models.Model):
    ROLES = (
        ('instructor', _('Instructor')),
        ('assistant', _('Assistant')),
        ('pedagogy_assistant', _('Pedagogy Assistant')),
    )

    user = models.ForeignKey(TimtecUser, verbose_name=_('Professor'))
    course = models.ForeignKey(Course, verbose_name=_('Course'))
    biography = models.TextField(_('Biography'), blank=True)
    role = models.CharField(_('Role'), choices=ROLES, default=ROLES[0][0], max_length=128)

    class Meta:
        unique_together = (('user', 'course'),)
        verbose_name = _('Course Professor')
        verbose_name_plural = _('Course Professors')

    def __unicode__(self):
        return u'%s @ %s' % (self.user, self.course)

    def new_message(self, course, subject, message, to=[]):
        return ProfessorMessage.objects.create(subject=subject,
                                               message=message,
                                               course=course,
                                               users=to,
                                               professor=self)


class ProfessorMessage(models.Model):
    professor = models.ForeignKey(TimtecUser, verbose_name=_('Professor'))
    users = models.ManyToManyField(TimtecUser, related_name='messages')
    subject = models.CharField(_('Subject'), max_length=255)
    message = models.TextField(_('Message'))
    date = models.DateTimeField(_('Date'), auto_now_add=True)
    course = models.ForeignKey(Course, verbose_name=_('Course'), null=True)

    def send(self):
        to = [u.email for u in self.users.all()]
        try:
            et = EmailTemplate.objects.get(name='professor-message')
        except EmailTemplate.DoesNotExist:
            et = EmailTemplate(name="professor-message", subject="{{subject}}", template="{{message}}")
        subject = Template(et.subject).render(Context({'subject': self.subject}))
        message = Template(et.template).render(Context({'message': self.message}))
        return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to, fail_silently=False)


class PositionedModel(models.Model):
    collection_name = 'pk'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            filters = {self.collection_name: getattr(self, self.collection_name)}
            latest = self.__class__.objects.filter(**filters) \
                .aggregate(models.Max('position')) \
                .get('position__max')

            if latest is not None:
                self.position = latest + 1

        return super(PositionedModel, self).save(*args, **kwargs)


class Lesson(PositionedModel):
    STATES = (
        ('draft', _('Draft')),
        ('listed', _('Listed')),
        ('published', _('Published')),
    )

    course = models.ForeignKey(Course, verbose_name=_('Course'), related_name='lessons')
    desc = models.TextField(_('Description'))
    name = models.CharField(_('Name'), max_length=255)
    notes = models.TextField(_('Notes'), default="", blank=True)
    position = models.IntegerField(default=0)
    slug = AutoSlugField(_('Slug'), populate_from='name', max_length=255, editable=False, unique=True)
    status = models.CharField(_('Status'), choices=STATES, default=STATES[0][0], max_length=64)

    collection_name = 'course'

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        ordering = ['position']

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
        from activities.models import Activity
        return Activity.objects.filter(unit__lesson=self).count()

    def unit_count(self):
        return self.units.all().count()

    def video_count(self):
        return self.units.exclude(video=None).count()

    def is_ready(self):
        return self.status == 'published' and self.units.exists()


class Unit(PositionedModel):
    title = models.CharField(_('Title'), max_length=128, blank=True)
    lesson = models.ForeignKey(Lesson, verbose_name=_('Lesson'), related_name='units')
    video = models.ForeignKey(Video, verbose_name=_('Video'), null=True, blank=True)
    activity = models.ForeignKey('activities.Activity', verbose_name=_('Activity'), null=True, blank=True, related_name='units')
    side_notes = models.TextField(_('Side notes'), blank=True)
    position = models.IntegerField(default=0)
    notes = generic.GenericRelation(Note)

    collection_name = 'lesson'

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ['lesson', 'position']

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.lesson, self.position, self.video, self.activity)


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


class EmailTemplate(models.Model):
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=255)
    template = models.TextField()
