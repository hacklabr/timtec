# -*- coding: utf-8 -*-
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse
from core.models import Course
from braces.views import LoginRequiredMixin, GroupRequiredMixin


class AdminCourseView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Course
    template_name = '_base.html'
    group_required = u'professors'

    def get_redirect_field_name(self):
        """
        Override this method to customize the redirect_field_name.
        """
        return reverse('course_intro', args=[self.kwargs['slug']])
