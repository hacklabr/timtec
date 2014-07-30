# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from core.models import Course
from course_material.forms import FileForm
from course_material.serializers import CourseMaterialSerializer
from course_material.models import CourseMaterial, File
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from rest_framework import viewsets
from rest_framework import filters
import json
from administration.views import AdminMixin


class CourseMaterialView(LoginRequiredMixin, DetailView):
    model = CourseMaterial
    context_object_name = 'course_material'
    template_name = 'course-material.html'
    slug_field = 'course__slug'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseMaterialView, self).get_context_data(**kwargs)
        self.course = get_object_or_404(Course, slug=self.kwargs['slug'])
        context['course'] = self.course
        return context


class FileUploadView(LoginRequiredMixin, FormView):
    form_class = FileForm


class CourseMaterialAdminView(AdminMixin, DetailView):
    model = CourseMaterial
    context_object_name = 'course_material'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseMaterialAdminView, self).get_context_data(**kwargs)
        self.course = get_object_or_404(Course, id=self.kwargs['pk'])
        context['course'] = self.course
        return context


class CourseMaterialViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = CourseMaterial
    serializer_class = CourseMaterialSerializer
    lookup_field = 'course'
    filter_fields = ('course__id',)
    filter_backends = (filters.DjangoFilterBackend,)

    def pre_save(self, obj):
        # Get Question vote usign kwarg as questionId
        if 'course' in self.kwargs:
            obj.course = Course.objects.get(id=int(self.kwargs['course']))
            self.kwargs['course'] = obj.course
        return super(CourseMaterialViewSet, self).pre_save(obj)
