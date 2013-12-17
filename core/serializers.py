from core.models import Course, CourseProfessor, CourseStudent, Lesson, Video, StudentProgress, Unit
from accounts.serializers import TimtecUserSerializer
from activities.serializers import ActivitySerializer
from rest_framework.reverse import reverse
from notes.models import Note
from rest_framework import serializers


class CourseProfessorSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer()

    class Meta:
        fields = ('id', 'user', 'biography', 'role',)
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
    intro_video = VideoSerializer(required=False)
    thumbnail_url = serializers.Field(source='get_thumbnail_url')
    professors = CourseProfessorSerializer(source='courseprofessor_set', many=True, allow_add_remove=True)

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status",
                  "thumbnail_url", "publication", "professors",)


class CourseThumbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "thumbnail",)


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


class LessonHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    # Need to do this because the rest framework doesnt support multiple
    # lookups
    def get_url(self, obj, view_name, request, format):
        kwargs = {'slug': obj.slug, 'course_slug': obj.course.slug}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.SlugRelatedField(slug_field='slug')
    units = UnitSerializer(many=True, allow_add_remove=True)
    thumbnail = serializers.Field(source='thumbnail')
    url = LessonHyperlinkedIdentityField(
        view_name='lesson',
        lookup_field='slug'
    )

    class Meta:
        model = Lesson
        fields = ('id', 'course', 'desc', 'name', 'notes', 'position', 'slug', 'status', 'units', 'url', 'thumbnail')


class SimplifiedLessonSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(slug_field='slug')

    class Meta:
        model = Lesson
        fields = ('id', 'course', 'name', 'position', 'slug')


class SimplifiedUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = ('id', 'title', 'position',)


class NoteUnitSerializer(serializers.ModelSerializer):

    content_object = UnitSerializer(read_only=True)
    lesson = serializers.SerializerMethodField('get_lesson')

    class Meta:
        model = Note
        fields = ('id', 'text', 'content_type', 'object_id', 'content_object', 'lesson')

    def get_lesson(self, obj):
        return SimplifiedLessonSerializer(obj.content_object.lesson).data
