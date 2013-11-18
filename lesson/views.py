# -*- coding: utf-8 -*-
from accounts.utils import LoginRequiredMixin
from core.models import Answer, Lesson, StudentProgress, Unit
from django.views.generic import DetailView
from django.utils import timezone
from lesson.serializers import AnswerSerializer, LessonSerializer, StudentProgressSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson.html"


class LessonViewSet(viewsets.ModelViewSet):
    model = Lesson
    serializer_class = LessonSerializer
    filter_fields = ('course__slug',)

    def get_queryset(self):
        queryset = super(LessonViewSet, self).get_queryset()
        if self.request.user.is_active:
            return queryset
        return queryset.filter(published=True)


class StudentProgressViewSet(viewsets.ModelViewSet):
    model = StudentProgress
    serializer_class = StudentProgressSerializer
    filter_fields = ('unit__lesson',)

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(StudentProgressViewSet, self).pre_save(obj)

    def get_queryset(self):
        user = self.request.user
        return StudentProgress.objects.filter(user=user)


class UpdateStudentProgressView(APIView):
    model = StudentProgress

    def post(self, request, unitId=None):
        user = request.user

        try:
            unit = Unit.objects.get(id=unitId)
        except Unit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = {}
        if not unit.activity:
            progress, created = StudentProgress.objects.get_or_create(user=user, unit=unit)
            progress.complete = timezone.now()
            progress.save()
            response['msg'] = 'Unit completed.'
            response['complete'] = progress.complete
        return Response(response, status=status.HTTP_201_CREATED)


class AnswerViewSet(viewsets.ModelViewSet):
    model = Answer
    serializer_class = AnswerSerializer
    filter_fields = ('activity', 'user',)

    def pre_save(self, obj):
        obj.user = self.request.user

    def post_save(self, obj, **kwargs):
        unit = self.request.DATA.get('unit', None)
        user = self.request.user
        progress, created = StudentProgress.objects.get_or_create(user=user, unit_id=unit)

        if obj.is_correct():
            progress.complete = timezone.now()
        progress.save()

    def get_queryset(self):
        return Answer.objects.all()
