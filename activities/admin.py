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
    list_display = ('type', 'question', '__unicode__', 'unit_title', 'unit_lesson', 'unit_position')

    def unit_title(self, object):
        return object.units.first().title

    def unit_lesson(self, object):
        return object.units.first().lesson.name

    def unit_position(self, object):
        return object.units.first().position


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Answer)
