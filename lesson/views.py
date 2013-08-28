# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from core.models import Lesson


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "lesson.html"
