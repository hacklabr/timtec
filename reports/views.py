# -*- coding: utf-8 -*-
from rest_framework import viewsets
from braces.views import LoginRequiredMixin
from core.models import Course, CourseStudent
from reports.serializer import UserCourseStats, CourseStats


class UserCourseStats(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    model = CourseStudent
    serializer_class = UserCourseStats
    filter_fields = ('course',)


class CourseStatsByLessonViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    model = Course
    serializer_class = CourseStats
