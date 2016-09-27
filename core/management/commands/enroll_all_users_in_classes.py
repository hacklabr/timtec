# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Class, CourseStudent


class Command(BaseCommand):
    args = ''
    help = 'All users in classes will be enrolled in its respective courses.'

    @transaction.atomic
    def handle(self, *args, **options):

        # List all classes
        classes = Class.objects.all()

        # Iterate classes
        for one_class in classes:
            # Iterate students in class
            for student in one_class.students.all():
                # Check if student has CourseStudent relationship for the given course_material
                try:
                    CourseStudent.objects.get(user=student, course=one_class.course)
                except CourseStudent.DoesNotExist:
                    # If there is none, create it
                    CourseStudent.objects.create(user=student, course=one_class.course)
                    pass
