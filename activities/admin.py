from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from .models import Answer, Activity


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'class': 'span12'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'class': 'span12'})},
    }


class ActivityAdmin(ModelAdmin):
    search_fields = ('type', 'data')
    list_display = ('lesson', 'unit', 'unit_position', 'type', 'question', '__unicode__')
    readonly_fields = ('unit_position', 'lesson')

    def unit(self, object):
        try:
            return object.units.first().title
        except AttributeError:
            return

    def lesson(self, object):
        try:
            return object.units.first().lesson.name
        except AttributeError:
            return

    def unit_position(self, object):
        try:
            return object.units.first().position
        except AttributeError:
            return


class AnswerAdmin(ModelAdmin):
    ordering = ('timestamp',)
    list_display = ('activity', 'user', 'timestamp', 'given', 'unit')
    readonly_fields = ('unit',)

    def unit(self, object):
        try:
            return object.activity.units.first().title
        except AttributeError:
            return

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Answer, AnswerAdmin)
