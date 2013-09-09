# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from core.models import Lesson
from rest_framework import viewsets
from lesson.serializers import LessonSerializer
from accounts.utils import LoginRequiredMixin


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson.html"


class LessonViewSet(viewsets.ModelViewSet):
    model = Lesson
    serializer_class = LessonSerializer
