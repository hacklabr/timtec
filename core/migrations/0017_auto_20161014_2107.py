# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from core.models import CourseCertification

import string
import random
import django.utils.timezone


def change_link_hash_duplicate(apps, schema_editor):
    """Create all CourseCertification that not exists."""
    hashs = []
    for cc in CourseCertification.objects.all():
        if cc.link_hash in hashs:
            h = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
            cc.link_hash = h
            cc.save()
        hashs.append(cc.link_hash)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_course_groups'),
    ]

    operations = [
            migrations.AddField(
                model_name='coursestudent',
                name='start_date',
                field=models.DateTimeField(default=django.utils.timezone.now),
            ),
            migrations.RunPython(change_link_hash_duplicate),
    ]
