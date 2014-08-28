from course_material.models import CourseMaterial, File
from django.contrib import admin


class FileInline(admin.TabularInline):
    model = File
    extra = 1


class CourseMaterialAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('course', 'text')
    inlines = [
        FileInline,
    ]


class FileAdmin(admin.ModelAdmin):
    search_fields = ('file',)
    list_display = ('file', 'course_material')


admin.site.register(CourseMaterial, CourseMaterialAdmin)
admin.site.register(File, FileAdmin)
