from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'Adds a user named student and a user named professor with password = x'

    def handle(self, *args, **options):
        u, _ = User.objects.get_or_create(username='student')
        u.set_password("x")
        u.email = "student@timtec.com.br"
        u.groups = []
        u.save()
        u.groups.add(Group.objects.get(name="students"))
        u.save()

        u, _ = User.objects.get_or_create(username='professor')
        u.set_password("x")
        u.email = "professor@timtec.com.br"
        u.groups = []
        u.save()
        u.groups.add(Group.objects.get(name="professors"))
        u.save()
