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

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        new_file = File()
        new_file.course_material = get_object_or_404(CourseMaterial, course__slug=self.kwargs['slug'])
        form = FileForm(instance=new_file, **self.get_form_kwargs())
        if form.is_valid():
            form.save()
            data = {'success': 200}
            return self.render_to_json_response(data)
        else:
            data = {'error': 400}
            return self.render_to_json_response(data, status=400)


class CourseMaterialAdminView(LoginRequiredMixin, DetailView):
    model = CourseMaterial
    context_object_name = 'course_material'
    template_name = 'course-material-admin.html'

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
