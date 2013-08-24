from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from suit.admin import SortableTabularInline

from models import *

admin.site.register(TimtecUser, UserAdmin)
admin.site.register(Video)
admin.site.register(CourseProfessor)


class LessonInline(SortableTabularInline):
    model = Lesson
    sortable = 'position'


class CourseAdmin(ModelAdmin):
    inlines = (LessonInline,)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Activity)
admin.site.register(Unit)
admin.site.register(Answer)
