from core.models import Course, CourseProfessor, Lesson, Unit
from core.serializers import VideoSerializer
from activities.serializers import ActivityImportExportSerializer
from course_material.serializers import CourseMaterialImportExportSerializer
from rest_framework import serializers


class CourseProfessorImportExportSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='get_name')
    biography = serializers.Field(source='get_biography')
    picture = serializers.Field(source='get_picture_url')

    class Meta:
        model = CourseProfessor
        exclude = ('user', 'role')


class UnitImportExportSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    activities = ActivityImportExportSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = Unit


class LessonImportExportSerializer(serializers.ModelSerializer):
    units = UnitImportExportSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = Lesson


class CourseImportExportSerializer(serializers.ModelSerializer):
    lessons = LessonImportExportSerializer(many=True, allow_add_remove=True)
    course_professors = CourseProfessorImportExportSerializer(many=True, allow_add_remove=True)
    intro_video = VideoSerializer()
    course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        # exclude = ('students', 'default_class')
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_professors', 'lessons', 'course_material',)
