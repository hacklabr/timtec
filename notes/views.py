# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateView
from notes.models import Note
from notes.serializers import NoteSerializer
from rest_framework import viewsets


class NotesViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Note
    serializer_class = NoteSerializer
    filter_fields = ('content_type', 'object_id')

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(NotesViewSet, self).pre_save(obj)

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)


class UserNotesView(LoginRequiredMixin, TemplateView):
    template_name = 'notes.html'


class CourseNotesView(LoginRequiredMixin, TemplateView):
    template_name = 'course_notes.html'
