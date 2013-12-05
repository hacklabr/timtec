# -*- coding: utf-8 -*-
from django.contrib import admin
from notes.models import Note


class NoteAdmin(admin.ModelAdmin):
    model = Note


admin.site.register(Note, NoteAdmin)
