# -*- coding: utf-8 -*-
from django.contrib import admin
from notes.models import Note


class NoteAdmin(admin.ModelAdmin):
    search_fields = ('text', 'user__username')
    list_display = ('text', 'user', 'create_timestamp', 'last_edit_timestamp')


admin.site.register(Note, NoteAdmin)
