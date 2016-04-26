from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from django.db import connection
from django.db.utils import IntegrityError, ProgrammingError
from ifs.models import IfUser

ActiveUser = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'Migrate deprecated user model IfUser to a new user model'

    def handle(self, *args, **options):
        if ActiveUser is IfUser:
            return

        try:
            ifusers = IfUser.objects.all().order_by('-last_login')
        except ProgrammingError:  # Relation IfUser doesn't exist.
            return

        for ifuser in ifusers:
            ifuser.__class__ = ActiveUser
            try:
                ifuser.save()
            except IntegrityError:  # Duplicated e-mail, created by import_users
                pass
            
        c = connection.cursor()
        c.execute('drop table ifs_ifuser cascade')
