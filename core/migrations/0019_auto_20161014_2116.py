# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from core.models import CourseStudent, CourseCertification

import string
import random


def create_coursecertifications(apps, schema_editor):
    """Create all CourseCertification that not exists."""
    for cs in CourseStudent.objects.filter(certificate=None):
        h = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        receipt = CourseCertification(course_student=cs,
                                      course=cs.course,
                                      type=CourseCertification.TYPES[0][0],
                                      is_valid=True, link_hash=h)
        receipt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20161014_2116'),
    ]

    operations = [
        migrations.RunPython(create_coursecertifications),
    ]
