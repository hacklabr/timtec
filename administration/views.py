# -*- coding: utf-8 -*-
from accounts.utils import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from core.models import Course


class AdminCourseView(LoginRequiredMixin, UpdateView):
    model = Course
    template_name = '_base.html'
