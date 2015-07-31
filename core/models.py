# -*- coding: utf-8 -*-
from __future__ import division

import datetime

from django.db import models
from django.db.models import Count
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Template, Context
from django.contrib.contenttypes import generic
from django.conf import settings
from autoslug import AutoSlugField

from notes.models import Note
from course_material.models import CourseMaterial
from .utils import hash_name

import re


class Video(models.Model):
    name = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')

    def __unicode__(self):
        if self.unit.first():
            unit = self.unit.first()
            if unit.lesson:
                return u'Aula: {0} | Unidade: {1} | id youtube: {2}'.format(unit.lesson, unit, self.youtube_id)
        return self.youtube_id


class Class(models.Model):
    name = models.CharField(max_length=200)
    assistant = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Assistant'), related_name='professor_classes', null=True, blank=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='classes', blank=True)
    course = models.ForeignKey('Course', verbose_name=_('Course'))

    def __unicode__(self):
        return u'%s @ %s' % (self.name, self.course)

    def get_absolute_url(self):
        return reverse('class', kwargs={'pk': self.id})

    def add_students(self, *objs):
        for obj in objs:
            try:
                c = Class.objects.get(course=self.course, students=obj)
                c.students.remove(obj)
            except Class.DoesNotExist:
                pass
            self.students.add(obj)

    def remove_students(self, *objs):
        for obj in objs:
            self.students.remove(obj)
            if CourseStudent.objects.filter(course=self.course, user=obj).exists():
                self.course.default_class.students.add(obj)


class Course(models.Model):
    STATES = (
        ('draft', _('Draft')),
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
    thumbnail = models.ImageField(_('Thumbnail'), upload_to=hash_name('course_thumbnails', 'name'), null=True, blank=True)
    professors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='professorcourse_set', through='CourseProfessor')
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='authorcourses', through='CourseAuthor')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='studentcourse_set', through='CourseStudent')
    home_thumbnail = models.ImageField(_('Home thumbnail'), upload_to=hash_name('home_thumbnails', 'name'), null=True, blank=True)
    home_position = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(_('Start date'), default=None, blank=True, null=True)
    home_published = models.BooleanField(default=False)
    default_class = models.OneToOneField(Class, verbose_name=_('Default Class'), related_name='default_course', null=True, blank=True)

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
        if not Class.objects.filter(course=self, students=student).exists():
            self.default_class.students.add(student)

        if not CourseStudent.objects.filter(course=self, user=student).exists():
            CourseStudent.objects.create(course=self, user=student)

    def is_enrolled(self, user):
        return CourseStudent.objects.filter(course=self, user=user).exists()

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''

    def get_home_thumbnail_url(self):
        if self.home_thumbnail:
            return self.home_thumbnail.url
        return ''

    @property
    def has_started(self):
        if self.start_date and self.start_date <= datetime.date.today():
            return True
        else:
            return False

    def avg_lessons_users_progress(self, classes=None):
        if classes:
            student_enrolled = self.coursestudent_set.filter(user__classes__in=classes).count()
        else:
            student_enrolled = self.coursestudent_set.all().count()
        progress_list = []
        for lesson in self.lessons.all():
            lesson_progress = {}
            lesson_progress['name'] = lesson.name
            lesson_progress['slug'] = lesson.slug
            lesson_progress['position'] = lesson.position
            units_len = lesson.unit_count()
            # avoid zero divisfion
            if units_len and student_enrolled:
                units_done = StudentProgress.objects.exclude(complete=None).filter(unit__lesson=lesson)
                if classes:
                    units_done = units_done.filter(user__classes__in=classes)
                units_done_len = units_done.count()
                lesson_progress['progress'] = 100 * units_done_len / (units_len * student_enrolled)
                # lesson_progress['forum_questions'] = lesson.forum_questions.count()
                # lesson_progress['progress'] =
                # lesson_progress['finish'] = self.get_lesson_finish_time(lesson)
            else:
                lesson_progress['progress'] = 0
                # lesson_progress['finish'] = ''
            progress_list.append(lesson_progress)
        return progress_list

    def forum_answers_by_lesson(self):
        return self.user.forum_answers.values('question__lesson').annotate(Count('question__lesson'))

    def get_video_professors(self):
        return self.course_authors.all()

    def get_professor_role(self, user):
        try:
            cp = self.course_professors.get(user=user)
            return cp.role
        except CourseProfessor.DoesNotExist:
            return False

    def get_role_professors(self, role):
        try:
            cp_set = self.course_professors.filter(role=role)
        except CourseProfessor.DoesNotExist:
            return False

        professors = []
        for cp in cp_set:
            professors.append(cp.user)

        return iter(professors)

    def is_assistant_or_coordinator(self, user):
        if user.is_staff or user.is_superuser:
            return True
        role = self.get_professor_role(user)
        return role in ['assistant', 'coordinator'] or user.is_superuser

    def is_course_coordinator(self, user):
        course_coordinators = self.get_role_professors('coordinator')

        return user.is_superuser or user.is_staff or user in course_coordinators

    def has_perm_own_all_classes(self, user):
        role = self.get_professor_role(user)
        return role == 'coordinator' or user.is_superuser

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super(Course, self).save(*args, **kwargs)

        if is_new:
            c = Class.objects.create(name=self.name, course=self)
            self.default_class = c
            self.save()
            CourseMaterial.objects.create(course=self)


class CourseStudent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Student'))
    course = models.ForeignKey(Course, verbose_name=_('Course'))

    class Meta:
        unique_together = (('user', 'course'),)
        ordering = ['course__start_date']

    def __unicode__(self):
        return u'{0} - {1}'.format(self.course, self.user)

    @property
    def units_done(self):
        return StudentProgress.objects.exclude(complete=None)\
                                      .filter(user=self.user, unit__lesson__course=self.course)

    def resume_next_unit(self):
        try:
            last_unit_done = self.units_done.latest('complete')
            # try to get the next unit in same lesson
            next_unit = Unit.objects.filter(lesson=last_unit_done.unit.lesson,
                                            position__gt=last_unit_done.unit.position).order_by('position').first()

            if next_unit:
                return next_unit
            else:
                next_lesson = self.course.lessons.filter(position__gt=last_unit_done.unit.lesson.position).order_by('position').first()
                if next_lesson and next_lesson.first_unit():
                    return next_lesson.units.order_by('position').first()
                else:
                    return self.course.first_lesson().first_unit()
        except StudentProgress.DoesNotExist:
            first_lesson = self.course.first_lesson()
            if first_lesson:
                return first_lesson.first_unit()
        except AttributeError:
            pass
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
        # TODO refator to make one query to count unts done for all lessons
        progress_list = []
        for lesson in self.course.lessons.filter(status='published'):
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
        ('coordinator', _('Professor Coordinator')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Professor'), related_name='teaching_courses', blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name=_('Course'), related_name='course_professors')
    biography = models.TextField(_('Biography'), blank=True, null=True)
    role = models.CharField(_('Role'), choices=ROLES, default=ROLES[1][0], max_length=128)
    picture = models.ImageField(_('Picture'), upload_to=hash_name('bio-pictures', 'name'), blank=True, null=True)
    name = models.TextField(_('Name'), max_length=30, blank=True, null=True)
    is_course_author = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'course'),)
        verbose_name = _('Course Professor')
        verbose_name_plural = _('Course Professors')

    def __unicode__(self):
        return u'%s @ %s' % (self.user, self.course)

    def get_name(self):
        if self.name:
            return self.name
        elif self.user:
            return self.user.get_full_name()

    def get_biography(self):
        if self.biography:
            return self.biography
        elif self.user:
            return self.user.biography

    def get_picture_url(self):
        if self.picture:
            location = "/%s/%s" % (settings.MEDIA_URL, self.picture)
            return re.sub('/+', '/', location)
        elif self.user:
            return self.user.get_picture_url()

    def new_message(self, course, subject, message, to=[]):
        return ProfessorMessage.objects.create(subject=subject,
                                               message=message,
                                               course=course,
                                               users=to,
                                               professor=self)

    def get_current_user_classes(self):
        return Class.objects.filter(course=self.course, assistant=self.user)


class CourseAuthor(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Professor'),
        related_name='authoring_courses',
        blank=True,
        null=True
    )
    course = models.ForeignKey(Course, verbose_name=_('Course'), related_name='course_authors')
    biography = models.TextField(_('Biography'), blank=True, null=True)
    picture = models.ImageField(_('Picture'), upload_to=hash_name('bio-pictures', 'name'), blank=True, null=True)
    name = models.TextField(_('Name'), max_length=30, blank=True, null=True)
    position = models.IntegerField(default=100, null=True, blank=True)

    class Meta:
        unique_together = (('user', 'course'),)
        verbose_name = _('Course Author')
        verbose_name_plural = _('Course Authors')
        ordering = ['position']

    def __unicode__(self):
        return u'%s @ %s' % (self.user, self.course)

    def get_name(self):
        if self.name:
            return self.name
        elif self.user:
            return self.user.get_full_name()

    def get_biography(self):
        if self.biography:
            return self.biography
        elif self.user:
            return self.user.biography

    def get_picture_url(self):
        if self.picture:
            location = "/%s/%s" % (settings.MEDIA_URL, self.picture)
            return re.sub('/+', '/', location)
        elif self.user:
            return self.user.get_picture_url()


class ProfessorMessage(models.Model):
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Professor'))
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='messages')
    subject = models.CharField(_('Subject'), max_length=255)
    message = models.TextField(_('Message'))
    date = models.DateTimeField(_('Date'), auto_now_add=True)
    course = models.ForeignKey(Course, verbose_name=_('Course'), null=True)

    def send(self):
        bcc = [u.email for u in self.users.all()]
        try:
            et = EmailTemplate.objects.get(name='professor-message')
        except EmailTemplate.DoesNotExist:
            et = EmailTemplate(name="professor-message", subject="{{subject}}", template="{{message}}")
        subject = Template(et.subject).render(Context({'subject': self.subject}))
        message = Template(et.template).render(Context({'message': self.message}))
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, None, bcc)
        return email.send()


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

    def first_unit(self):
        if self.units.exists():
            try:
                return self.units.order_by('position').first()
            except AttributeError:
                return None


class Unit(PositionedModel):
    title = models.CharField(_('Title'), max_length=128, blank=True)
    lesson = models.ForeignKey(Lesson, verbose_name=_('Lesson'), related_name='units')
    video = models.ForeignKey(Video, verbose_name=_('Video'), related_name='unit', null=True, blank=True)
    side_notes = models.TextField(_('Side notes'), blank=True)
    position = models.IntegerField(default=0)
    notes = generic.GenericRelation(Note)

    collection_name = 'lesson'

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ['lesson', 'position']

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.position)


class StudentProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Student'))
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
