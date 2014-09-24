from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import unicodecsv

User = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'import users'

    def handle(self, *args, **options):
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
                nu.save()
