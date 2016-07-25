# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from notes.models import Note
from notes.serializers import NoteSerializer
from core.models import Course
from rest_framework import viewsets


class NotesViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Note
    serializer_class = NoteSerializer
    filter_fields = ('content_type', 'object_id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(NotesViewSet, self).pre_save(obj)

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)


class UserNotesView(LoginRequiredMixin, TemplateView):
    template_name = 'notes.html'


class CourseNotesView(LoginRequiredMixin, TemplateView):
    template_name = 'course-notes.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseNotesView, self).get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return context
