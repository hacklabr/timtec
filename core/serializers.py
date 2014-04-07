from core.models import Course, CourseProfessor, CourseStudent, Lesson, Video, StudentProgress, Unit, ProfessorMessage
from accounts.serializers import TimtecUserSerializer
from activities.serializers import ActivitySerializer
from rest_framework.reverse import reverse
from notes.models import Note
from rest_framework import serializers


class CourseProfessorSerializer(serializers.ModelSerializer):
    user_info = TimtecUserSerializer(source='user', read_only=True)

    class Meta:
        fields = ('id', 'course', 'user', 'user_info', 'biography', 'role',)
        model = CourseProfessor


class ProfessorMessageSerializer(serializers.ModelSerializer):

    professor = TimtecUserSerializer(source='professor', read_only=True)
    users_details = TimtecUserSerializer(source='users', read_only=True)

    class Meta:
        model = ProfessorMessage
        fields = ('id', 'course', 'users', 'subject', 'message', 'date', 'users_details',)


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
    professor_name = serializers.SerializerMethodField('get_professor_name')
    home_thumbnail_url = serializers.SerializerMethodField('get_home_thumbnail_url')
    professors_names = serializers.SerializerMethodField('get_professors_names')

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status",
                  "thumbnail_url", "publication", "home_thumbnail_url", "home_position",
                  "start_date", "professor_name", "home_published", "professors_names")

    @staticmethod
    def get_professor_name(obj):
        if obj.professors.all():
            return obj.professors.all()[0]
        return ''

    @staticmethod
    def get_professors_names(obj):
        professors = obj.professors.all()
        if professors:
            if len(professors) > 1:
                return '{0} e {1}'.format(professors[0], professors[1])
            else:
                return professors[0]
        return ''

    @staticmethod
    def get_home_thumbnail_url(obj):
        if obj.home_thumbnail:
            return obj.home_thumbnail.url
        return ''


class CourseThumbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "thumbnail",)


class StudentProgressSerializer(serializers.ModelSerializer):
    complete = serializers.DateTimeField(required=False)

    class Meta:
        model = StudentProgress
        fields = ('unit', 'complete',)


class UnitSerializer(serializers.ModelSerializer):
    video = VideoSerializer(required=False)
    activities = ActivitySerializer(many=True, allow_add_remove=True)

    class Meta:
        model = Unit
        fields = ('id', 'title', 'video', 'activities', 'side_notes', 'position',)


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


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('id', 'text', 'content_type', 'object_id',)


class UnitNoteSerializer(serializers.ModelSerializer):

    user_note = NoteSerializer()

    class Meta:
        model = Unit
        fields = ('id', 'title', 'video', 'position', 'user_note')


class LessonNoteSerializer(serializers.ModelSerializer):

    units_notes = UnitNoteSerializer()
    course = serializers.SlugRelatedField(slug_field='slug')

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'position', 'slug', 'course', 'units_notes',)


class CourseNoteSerializer(serializers.ModelSerializer):

    lessons_notes = LessonNoteSerializer()
    course_notes_number = serializers.IntegerField(required=False)

    class Meta:
        model = Course
        fields = ('id', 'slug', 'name', 'lessons_notes', 'course_notes_number',)
