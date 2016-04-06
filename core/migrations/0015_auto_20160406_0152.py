# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_certificate_templates(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Course = apps.get_model("core", "Course")
    CertificateTemplate = apps.get_model("core", "IfCertificateTemplate")
    for course in Course.objects.all():
        if not CertificateTemplate.objects.filter(course=course).exists():
            CertificateTemplate.objects.create(course=course)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20160317_2130'),
    ]

    operations = [
        migrations.RunPython(create_certificate_templates),
    ]
