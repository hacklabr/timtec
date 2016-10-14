# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from core.models import CourseStudent, CourseCertification

from base64 import urlsafe_b64encode as ub64
from hashlib import sha1
from time import time


def create_coursecertifications(apps, schema_editor):
    """Create all CourseCertification that not exists."""
    for cs in CourseStudent.objects.filter(certificate=None):

        h = ub64(sha1(str(time()) + cs.user.last_name.encode('utf-8')).digest()[0:6])
        receipt = CourseCertification(course_student=cs,
                                      course=cs.course,
                                      type=CourseCertification.TYPES[0][0],
                                      is_valid=True, link_hash=h)
        receipt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_class_user_can_certificate_even_without_progress'),
    ]

    operations = [
            migrations.RunPython(create_coursecertifications),
    ]
