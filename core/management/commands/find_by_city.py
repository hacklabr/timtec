# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    args = ''
    help = 'Remove all student related data'

    def handle(self, *args, **options):

        cities = []

        for city in cities:
            users = User.objects.filter(city=city)
            if users:
                for user in users:
                    print user.username
