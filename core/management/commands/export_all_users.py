# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import csv

User = get_user_model()


def get_model_fields(model):
    return model._meta.fields


class Command(BaseCommand):
    args = ''
    help = 'Export all users data to a CSV file'

    def handle(self, *args, **options):
        with open('users_data.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            fields = get_model_fields(User)
            writer.writerow(fields)

            for obj in User.objects.all():
                row = []
                for field in fields:
                    try:
                        row.append(str(getattr(obj, field.name).encode('utf-8')))
                    except Exception as e:
                        row.append(str(getattr(obj, field.name)))
                # Get user groups
                row.append(obj.groups.all())
                writer.writerow(row)
