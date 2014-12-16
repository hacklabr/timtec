# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model, models
from django.db import transaction

import unicodecsv

User = get_user_model()

sizes = {
    'username': 30,
    'last_name': 30,
    'first_name': 30,
}


class Command(BaseCommand):
    args = 'file'
    help = 'import users'

    @transaction.atomic
    def handle(self, *files, **options):

        if not len(files) == 1:
            raise CommandError('No file to import')

        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            count = 0
            for row in readf:
                for fieldname, size in sizes.items():
                    if fieldname in row:
                        row[fieldname] = row[fieldname][:size]
                set_password = row.pop('set_password')
                nu = User.objects.create(**row)
                nu.set_password(set_password)
                nu.is_if_staff = True
                nu.save()
                if nu.cpf:  # only valid for IfUsers, remove if you don't need it
                    nu.groups.add(models.Group.objects.get(name="professors"))
                count += 1
                if count % 10 == 0:
                    print '.',
