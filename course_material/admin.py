from course_material.models import CourseMaterial
from django.contrib import admin


class CourseMaterialAdmin(admin.ModelAdmin):
    model = CourseMaterial


admin.site.register(CourseMaterial, CourseMaterialAdmin)
