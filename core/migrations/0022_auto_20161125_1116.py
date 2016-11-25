# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_assistants(apps, schema_editor):
    Class = apps.get_model("core", "Class")
    for class_group in Class.objects.all():
        if class_group.assistant:
            class_group.assistants.add(class_group.assistant)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_class_assistants'),
    ]

    operations = [
        migrations.RunPython(migrate_assistants),
    ]
