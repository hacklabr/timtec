# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from core.models import CourseStudent, CourseCertification

import string
import random


def create_coursecertifications(apps, schema_editor):
    """Create all CourseCertification that not exists."""
    # You must call "values_list" in a data migration whenever possible, since the model Class can have new fields that aren't present in the database at the moment of this migration
    for cs in CourseStudent.objects.filter(certificate=None).values_list('user_id', 'course_id'):
        h = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        receipt = CourseCertification(course_student_id=cs[0],  # user_id
                                      course_id=cs[1],  # course_id
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
