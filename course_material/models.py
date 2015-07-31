# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CourseMaterial(models.Model):
    course = models.OneToOneField('core.Course', related_name='course_material', verbose_name=_('Course Materials'))
    text = models.TextField(_('Question'))

    class Meta:
        unique_together = ("id", "course")

    def __unicode__(self):
        return self.course.name


def get_upload_path(instance, filename):
    return u'{0}/{1}'.format(instance.course_material.course.slug, filename)


class File(models.Model):
    # title = models.CharField(_('Title'), max_length=255)
    file = models.FileField(upload_to=get_upload_path)
    course_material = models.ForeignKey(CourseMaterial, related_name='files', verbose_name=_('Files'))
