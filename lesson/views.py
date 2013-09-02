# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from core.models import Lesson

from accounts.utils import LoginRequiredMixin

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson.html"
