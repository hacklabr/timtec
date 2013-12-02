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


class UserNotesView(LoginRequiredMixin, TemplateView):
    template_name = 'notes.html'


class NoteView(LoginRequiredMixin, TemplateView):
    template_name = 'note.html'
