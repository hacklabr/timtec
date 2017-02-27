# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model, models
from django.db import transaction

import unicodecsv
import random

User = get_user_model()

collumns = [
    'RF',
    'name',
    'job',
    'cell',
    'email',
]


class Command(BaseCommand):
    args = 'file'
    help = 'import users'

    @transaction.atomic
    def handle(self, *files, **options):

        if not len(files) == 1:
            raise CommandError('No file to import')

        group, _ = models.Group.objects.get_or_create(name="Associados")

        with open(files[0], 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            count = 0

            emails = []
            usernames = []
            for row in readf:
                if row.has_key('email') and row.get('email'):
                    email = row.get('email')
                    if email in emails:
                        self.stdout.write(u'Email ja existe: ' + email)
                    else:
                        emails.append(email)

                    cpf = row.get('cpf')
                    if User.objects.filter(username=cpf).exists():
                        self.stdout.write(u'Usuário ja existe: ' + cpf)
                    else:
                        usernames.append(cpf)

                user = User()
                user.first_name, user.last_name = row.get('name').split(' ', 1 )
                if user.first_name:
                    user.first_name = user.first_name.title()
                if user.last_name:
                    user.last_name = user.last_name.title()
                if row.has_key('email') and row.get('email'):
                    user.email = row.get('email')
                else:
                    user.email = str(random.randint(1,100000000)) + '@nomail.com'

                if row.has_key('occupation'):
                    user.occupation = row.get('occupation')
                cpf = row.get('cpf')
                user.username = user.cpf = cpf
                user.rg = row.get('RF')
                user.is_active = False
                user.save()
                user.groups.add(group)
                user.save()

                count += 1
                if count % 100 == 0:
                    self.stdout.write(str(count))
