# -*- coding: utf-8 -*-
from django.db import models
from core.models import Course
from django.utils.translation import ugettext_lazy as _


class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='course_material', verbose_name=_('Course Materials'))
    text = models.TextField(_('Question'))


def get_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.course_material.course.slug, filename)


class File(models.Model):
    # title = models.CharField(_('Title'), max_length=255)
    file = models.FileField(upload_to=get_upload_path)
    course_material = models.ForeignKey(CourseMaterial, related_name='files', verbose_name=_('Files'))
