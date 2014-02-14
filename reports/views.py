# -*- coding: utf-8 -*-
from rest_framework import viewsets
from braces.views import LoginRequiredMixin
from core.models import CourseStudent
from reports.serializer import UserCourseStats


class UserCourseStats(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    model = CourseStudent
    serializer_class = UserCourseStats
    filter_fields = ('course',)
    # lookup_field = 'course__id'
