# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.base import RedirectView, View, TemplateView
from accounts.utils import LoginRequiredMixin

from models import Course


class HomeView(View):
    def get(self, request):
        latest = Course.objects.latest('publication')
        return redirect(reverse('course_intro', args=[latest.slug]))


class CourseIntroView(DetailView):
    model = Course
    template_name = 'course-intro.html'


class UserCoursesView(LoginRequiredMixin,TemplateView):
    template_name = 'user-courses.html'


class EnrollCourseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        self.object = Course.objects.get(**self.kwargs)
        return self.object

    def get_redirect_url(self, **kwargs):
        course = self.get_object()
        course.enroll_student(self.request.user)
        return reverse('lesson', args=[course.first_lesson().slug])
