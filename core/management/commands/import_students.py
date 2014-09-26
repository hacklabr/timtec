# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings

import unicodecsv

User = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'import users'

    def handle(self, *args, **options):
        try:
            default_group = Group.objects.get(name=settings.REGISTRATION_DEFAULT_GROUP_NAME)
        except ObjectDoesNotExist:
            print "Grupo padrão não configurado. Verifique a variável " \
                  "REGISTRATION_DEFAULT_GROUP_NAME no arquivo settings.py e se o grupo exite"
        with open('../ifsul.csv', 'r') as csvfile:
            readf = unicodecsv.DictReader(csvfile)
            for row in readf:
                for i in ['username',
                          'last_name',
                          'first_name']:
                    if i in row:
                        row[i] = row[i][:30]
                nu = User.objects.create(**row)
                nu.set_password('x')
                nu.groups.add(default_group)
                nu.is_if_staff = True
                nu.save()
