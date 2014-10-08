# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from core.models import Course, CourseStudent, Class
from reports.serializer import UserCourseStatsSerializer, CourseStats, LessonUserStats


class UserCourseStats(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    model = CourseStudent
    serializer_class = UserCourseStatsSerializer
    filter_fields = ('course',)

    def get_queryset(self):
        queryset = super(UserCourseStats, self).get_queryset()
        user = self.request.user
        course_id = self.request.QUERY_PARAMS.get('course')
        role = None
        if course_id:
            role = user.teaching_courses.get(course__id=course_id).role

        classes_id = self.request.QUERY_PARAMS.getlist('classes')
        # class passed as get paremeter
        classes = Class.objects.filter(course=course_id)
        if classes_id:
            classes = classes.filter(id__in=classes_id)
            queryset = queryset.filter(user__classes__in=classes)
        if role and role == 'coordinator':
            return queryset
        else:
            classes = classes.filter(assistant=user)
            return queryset.filter(user__classes__in=classes)


class UserCourseLessonsStats(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    model = CourseStudent
    serializer_class = LessonUserStats
    filter_fields = ('course', 'user',)
    lookup_field = 'course'


class CourseStatsByLessonViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    model = Course
    serializer_class = CourseStats

    def retrieve(self, request, *args, **kwargs):
        self.object = self.get_object()

        course_id = self.kwargs.get('pk')
        role = None
        if course_id:
            role = self.request.user.teaching_courses.get(course__id=course_id).role

        classes_id = self.request.QUERY_PARAMS.getlist('classes')
        # class passed as get paremeter
        classes = Class.objects.filter(course=course_id)
        if classes_id:
            classes = classes.filter(id__in=classes_id)
        if not role or not (role == 'coordinator'):
            classes = classes.filter(assistant=self.request.user)

        self.object.classes = classes
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)
