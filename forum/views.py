# -*- coding: utf-8 -*-
from accounts.utils import LoginRequiredMixin
from core.models import Course
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from forum.models import Question


# from models import Question


class CourseForumView(LoginRequiredMixin, ListView):
    context_object_name = 'questions'
    template_name = "forum.html"

    def get_queryset(self):
        self.course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return Question.objects.filter(course=self.course)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseForumView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['course'] = self.course
        return context
