from core.models import Course, CourseAuthor, Lesson, Unit
from core.serializers import VideoSerializer
from activities.serializers import ActivityImportExportSerializer
from course_material.serializers import CourseMaterialImportExportSerializer
from rest_framework import serializers


class CourseAuthorsExportSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='get_name')
    biography = serializers.Field(source='get_biography')
    picture = serializers.Field(source='get_picture_url')

    class Meta:
        model = CourseAuthor
        exclude = ('id', 'user', 'course',)


class CourseAuthorsImportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseAuthor
        exclude = ('id', 'user', 'course',)


class UnitImportExportSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    activities = ActivityImportExportSerializer(many=True)

    class Meta:
        model = Unit
        exclude = ('id', 'lesson',)

    def create(self, validated_data):
        activity_data = validated_data['activities']
        validated_data.pop('activities')
        validated_data['lesson'] = self.initial_data[0].lesson
        new_unit = super(UnitImportExportSerializer, self).create(validated_data)

        # If there are any activities in this unit, they must be saved
        if activity_data:
            for activity in activity_data:
                activity.unit = new_unit
            activities = ActivityImportExportSerializer(data=activity_data, many=True)

        return new_unit


class LessonImportExportSerializer(serializers.ModelSerializer):
    units = UnitImportExportSerializer(many=True)

    class Meta:
        model = Lesson
        exclude = ('id', 'course',)

    def create(self, validated_data):
        unit_data = validated_data['units']
        validated_data.pop('units')
        validated_data['course'] = self.initial_data[0].course
        new_lesson = super(LessonImportExportSerializer, self).create(validated_data)

        for unit in unit_data:
            unit.lesson = new_lesson

        units = UnitImportExportSerializer(data=unit_data, many=True)
        if units.is_valid():
            units.save()

        return new_lesson


class CourseExportSerializer(serializers.ModelSerializer):
    lessons = LessonImportExportSerializer(many=True)
    course_authors = CourseAuthorsExportSerializer(many=True)
    intro_video = VideoSerializer()
    course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_authors', 'lessons', 'course_material',)


class CourseImportSerializer(serializers.ModelSerializer):
    lessons = LessonImportExportSerializer(many=True)
    # course_authors = CourseAuthorsImportSerializer(many=True, read_only=True)
    intro_video = VideoSerializer(read_only=True)
    # course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_authors', 'lessons',)

    def create(self, validated_data):

        lesson_data = validated_data.pop('lessons')
        new_course = super(CourseImportSerializer, self).create(validated_data)

        for lesson in lesson_data:
            lesson.course = new_course

        # Create lessons
        lessons = LessonImportExportSerializer(data=lesson_data, many=True)
        if lessons.is_valid():
            lessons.save()

        # Create course_authors

        # Create intro_video

        return new_course
