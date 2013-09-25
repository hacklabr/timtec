# -*- coding: utf-8 -*-
from accounts.utils import LoginRequiredMixin
from core.models import Lesson, StudentProgress, Unit
from django.views.generic import DetailView
from lesson.serializers import LessonSerializer, StudentProgressSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson.html"


class LessonViewSet(viewsets.ModelViewSet):
    model = Lesson
    serializer_class = LessonSerializer


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

class ReceiveAnswerView(APIView):

    def post(self, request, format=None):
        pass