# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import Textarea
from django.db import models
from activities.admin import ModelAdmin
from .models import *


class LessonInline(admin.TabularInline):
    model = Lesson
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 3, 'class': 'span11'})},
    }


class UnitInline(admin.TabularInline):
    model = Unit
    fields = ('title', 'video', 'position',)


class LessonAdmin(ModelAdmin):
    list_display = ('name', 'course',)
    search_fields = ('course__name',)
    inlines = (UnitInline,)


class UnitAdmin(ModelAdmin):
    search_fields = ('title', 'lesson__name')
    list_display = ('title', 'position', 'lesson', 'video',)
    list_select_related = ('lesson', 'video')


class CourseAdmin(ModelAdmin):
    list_display = ('name', 'status', 'start_date',)
    inlines = (LessonInline,)


class CourseProfessorAdmin(ModelAdmin):
    list_display = ('user', 'course',)


class VideoAdmin(ModelAdmin):
    list_display = ('name', 'youtube_id',)


class ClassAdmin(ModelAdmin):
    search_fields = ('name', 'course', 'assistant')
    list_display = ('name', 'assistant', 'course')
    filter_horizontal = ('students', )


class StudentProgressAdmin(ModelAdmin):
    search_fields = ('user__username',)
    list_display = ('user', 'unit', 'complete', 'last_access')


class CourseStudentAdmin(ModelAdmin):
    search_fields = ('user__username',)
    list_display = ('user', 'course')

admin.site.register(Video, VideoAdmin)
admin.site.register(CourseProfessor, CourseProfessorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(StudentProgress, StudentProgressAdmin)
admin.site.register(CourseStudent, CourseStudentAdmin)
admin.site.register(ProfessorMessage)
admin.site.register(Class, ClassAdmin)
