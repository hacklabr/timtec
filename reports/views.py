# -*- coding: utf-8 -*-
from rest_framework import viewsets
from braces.views import LoginRequiredMixin
from core.models import Lesson, CourseStudent
from reports.serializer import UserCourseStats


class UserCourseStats(LoginRequiredMixin, viewsets.ModelViewSet):
    model = CourseStudent
    serializer_class = UserCourseStats
    lookup_field = 'course'
