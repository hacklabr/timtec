# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from django.db import models

from suit.admin import SortableTabularInline

from models import *


class ModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'class': 'span12'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'class': 'span12'})},
    }


class LessonInline(admin.TabularInline):
    model = Lesson
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 3, 'class': 'span11'})},
    }


class UnitInline(admin.TabularInline):
    model = Unit
    fields = ('video', 'activity', 'position',)


class LessonAdmin(ModelAdmin):
    list_display = ('name', 'course',)
    inlines = (UnitInline,)


class UnitAdmin(ModelAdmin):
    list_display = ('position', 'lesson', 'video', 'activity',)


class CourseAdmin(ModelAdmin):
    list_display = ('name', 'status', 'publication',)
    inlines = (LessonInline,)


class CourseProfessorAdmin(ModelAdmin):
    list_display = ('user', 'course',)


class VideoAdmin(ModelAdmin):
    list_display = ('name', 'youtube_id',)


admin.site.register(TimtecUser, UserAdmin)

admin.site.register(Video, VideoAdmin)
admin.site.register(CourseProfessor, CourseProfessorAdmin)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Activity)
admin.site.register(Answer)
