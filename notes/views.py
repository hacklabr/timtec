# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin
from notes.models import Note
from notes.serializers import NoteSerializer
from rest_framework import viewsets


class NotesViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Note
    serializer_class = NoteSerializer
    filter_fields = ('course', 'user')

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(QuestionViewSet, self).pre_save(obj)
