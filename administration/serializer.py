from core.models import Course, CourseProfessor, Lesson, Unit
from core.serializers import VideoSerializer, CourseProfessorSerializer
from activities.serializers import ActivityImportExportSerializer
from course_material.serializers import CourseMaterialImportExportSerializer
from rest_framework import serializers


class CourseProfessorExportSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='get_name')
    biography = serializers.Field(source='get_biography')
    picture = serializers.Field(source='get_picture_url')

    class Meta:
        model = CourseProfessor
        exclude = ('user',)


class UnitImportExportSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    activities = ActivityImportExportSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = Unit


class LessonImportExportSerializer(serializers.ModelSerializer):
    units = UnitImportExportSerializer(many=True, allow_add_remove=True)

    class Meta:
        model = Lesson


class CourseExportSerializer(serializers.ModelSerializer):
    lessons = LessonImportExportSerializer(many=True, allow_add_remove=True)
    course_professors = CourseProfessorExportSerializer(CourseProfessor.objects.filter(role='instructor'),
                                                        many=True,
                                                        allow_add_remove=True,)
    intro_video = VideoSerializer()
    course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_professors', 'lessons', 'course_material',)


class CourseImportSerializer(serializers.ModelSerializer):
    lessons = LessonImportExportSerializer(many=True, allow_add_remove=True)
    course_professors = CourseProfessorSerializer(many=True, allow_add_remove=True)
    intro_video = VideoSerializer()
    course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_professors', 'lessons', 'course_material',)
