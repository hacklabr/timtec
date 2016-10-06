from core.models import Course, CourseAuthor, Lesson, Unit
from core.serializers import VideoSerializer
from activities.serializers import ActivityImportSerializer, ActivityExportSerializer
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


class UnitExportSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    activities = ActivityExportSerializer(many=True)

    class Meta:
        model = Unit
        exclude = ('id', 'lesson',)


class UnitImportSerializer(UnitExportSerializer):

    activities = ActivityImportSerializer(many=True)
    video = VideoSerializer(required=False, allow_null=True)

    def create(self, validated_data):
        activity_data = validated_data.pop('activities')
        video_data = validated_data.pop('video')
        validated_data['lesson'] = self.initial_data[0].lesson
        new_unit = super(UnitImportSerializer, self).create(validated_data)
        # If there is a video in this uint, it must be saved
        if video_data:
            video_ser = VideoSerializer(data=video_data)
            if video_ser.is_valid():
                video = video_ser.save()
                new_unit.video = video
                new_unit.save()

        # If there are any activities in this unit, they must be saved
        if activity_data:
            activities = ActivityImportSerializer(data=activity_data, many=True)
            if activities.is_valid():
                saved_activities = activities.save()

                for activity in saved_activities:
                    activity.unit = new_unit
                    activity.save()

        return new_unit


class LessonExportSerializer(serializers.ModelSerializer):
    units = UnitExportSerializer(many=True)

    class Meta:
        model = Lesson
        exclude = ('id', 'course',)


class LessonImportSerializer(LessonExportSerializer):
    units = UnitImportSerializer(many=True)

    def create(self, validated_data):
        unit_data = validated_data.pop('units')
        validated_data['course'] = self.initial_data[0].course
        new_lesson = super(LessonImportSerializer, self).create(validated_data)

        for unit in unit_data:
            unit.lesson = new_lesson

        units = UnitImportSerializer(data=unit_data, many=True)
        if units.is_valid():
            units.save()

        return new_lesson


class CourseExportSerializer(serializers.ModelSerializer):
    lessons = LessonExportSerializer(many=True)
    course_authors = CourseAuthorsExportSerializer(many=True)
    intro_video = VideoSerializer()
    course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_authors', 'lessons', 'course_material',)


class CourseImportSerializer(serializers.ModelSerializer):
    lessons = LessonImportSerializer(many=True)
    # course_authors = CourseAuthorsImportSerializer(many=True, read_only=True)
    intro_video = VideoSerializer()
    # course_material = CourseMaterialImportExportSerializer()

    class Meta:
        model = Course
        fields = ('slug', 'name', 'intro_video', 'application', 'requirement', 'abstract', 'structure',
                  'workload', 'pronatec', 'status', 'thumbnail', 'home_thumbnail', 'home_position',
                  'start_date', 'home_published', 'course_authors', 'lessons',)

    def create(self, validated_data):
        lesson_data = validated_data.pop('lessons')
        video_data = validated_data.pop('intro_video')

        new_course = super(CourseImportSerializer, self).create(validated_data)

        for lesson in lesson_data:
            lesson.course = new_course

        # Create lessons
        lessons = LessonImportSerializer(data=lesson_data, many=True)
        if lessons.is_valid():
            lessons.save()

        # Create intro_video
        video_ser = VideoSerializer(data=video_data)
        if video_ser.is_valid():
            video = video_ser.save()
            new_course.intro_video = video

        return new_course
