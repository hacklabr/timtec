from core.models import Course, CourseProfessor, CourseStudent, Lesson, Video, StudentProgress, Unit
from accounts.serializers import TimtecUserSerializer
from activities.serializers import ActivitySerializer
from rest_framework import serializers


class CourseProfessorSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer()

    class Meta:
        model = CourseProfessor


class CourseStudentSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer()

    class Meta:
        model = CourseStudent


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id', 'name', 'youtube_id',)


class CourseSerializer(serializers.ModelSerializer):
    intro_video = VideoSerializer()

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status", "publication",
                  "professors",)


class StudentProgressSerializer(serializers.ModelSerializer):
    complete = serializers.DateTimeField(required=False)

    class Meta:
        model = StudentProgress
        fields = ('unit', 'complete', 'last_access',)


class UnitSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    activity = ActivitySerializer()

    class Meta:
        model = Unit
        fields = ('id', 'title', 'video', 'activity', 'side_notes', 'position',)


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.SlugRelatedField(slug_field='slug')
    units = UnitSerializer(many=True, allow_add_remove=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='lesson',
        lookup_field='slug'
    )

    class Meta:
        model = Lesson
        fields = ('id', 'course', 'desc', 'name', 'notes', 'position', 'slug', 'status', 'units', 'url',)
