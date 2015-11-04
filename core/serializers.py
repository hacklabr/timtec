from django.contrib.flatpages.models import FlatPage
from core.models import (Course, CourseProfessor, CourseStudent, Lesson,
                         Video, StudentProgress, Unit, ProfessorMessage,
                         Class, CourseAuthor, CourseCertification,
                         CertificationProcess, Evaluation, IfCertificateTemplate)
from accounts.serializers import TimtecUserSerializer, \
    TimtecUserAdminCertificateSerializer
from activities.serializers import ActivitySerializer
from rest_framework.reverse import reverse_lazy
from notes.models import Note
from rest_framework import serializers


class ProfessorMessageSerializer(serializers.ModelSerializer):

    professor = TimtecUserSerializer(source='professor', read_only=True)
    users_details = TimtecUserSerializer(source='users', read_only=True)

    class Meta:
        model = ProfessorMessage
        fields = ('id', 'course', 'users', 'subject', 'message', 'date', 'users_details',)


class CourseCertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCertification
        fields = ('link_hash', 'created_date', 'is_valid')


class CertificationProcessSerializer(serializers.ModelSerializer):
    course_certification = CourseCertificationSerializer()
    student = TimtecUserAdminCertificateSerializer()

    class Meta:
        model = CertificationProcess


class EvaluationSerializer(serializers.ModelSerializer):
    processes = CertificationProcessSerializer(many=True, read_only=True)

    class Meta:
        model = Evaluation


class IfCertificateTemplateSerializer(serializers.ModelSerializer):
    logo_url = serializers.Field(source='get_logo_url')
    signature_url = serializers.Field(source='get_signature_url')

    class Meta:
        model = IfCertificateTemplate
        fields = ('id', 'course', 'pronatec_logo', 'mec_logo', 'if_name',
                  'signature_name', 'logo_url', 'signature_url',)

    def update(self, instance, validated_data):
        return super(IfCertificateTemplateSerializer, self)\
            .update(instance, validated_data)


class IfCertificateTemplateImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IfCertificateTemplate
        fields = ("logo", "signature")


class CourseStudentSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer()
    course_finished = serializers.BooleanField(source='course_finished')
    can_emmit_receipt = serializers.BooleanField(source='can_emmit_receipt')
    percent_progress = serializers.IntegerField(source='percent_progress')
    min_percent_to_complete = serializers.IntegerField(
        source='min_percent_to_complete')

    class Meta:
        model = CourseStudent
        fields = ('id', 'user', 'course', 'course_finished',
                  'can_emmit_receipt', 'percent_progress',
                  'min_percent_to_complete',)


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
    has_started = serializers.Field()

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status",
                  "thumbnail_url", "home_thumbnail_url", "home_position",
                  "start_date", "professor_name", "home_published",
                  "professors_names", "has_started",
                  "min_percent_to_complete")

    @staticmethod
    def get_professor_name(obj):
        if obj.professors.all():
            return obj.professors.all()[0]
        return ''

    @staticmethod
    def get_professors_names(obj):
        professors = obj.get_video_professors()
        if professors:
            if len(professors) > 1:
                return '{0} e {1}'.format(professors[0].user, professors[1].user)
            else:
                return professors[0].user
        return ''

    @staticmethod
    def get_home_thumbnail_url(obj):
        if obj.home_thumbnail:
            return obj.home_thumbnail.url
        return ''


class CourseThumbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "thumbnail", "home_thumbnail")


class StudentProgressSerializer(serializers.ModelSerializer):
    complete = serializers.DateTimeField(required=False)
    user = TimtecUserSerializer(read_only=True, source='user')

    class Meta:
        model = StudentProgress
        fields = ('unit', 'complete', 'user',)


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
        return reverse_lazy(view_name, kwargs=kwargs, request=request, format=format)


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.SlugRelatedField(slug_field='slug')
    units = UnitSerializer(many=True, allow_add_remove=True)
    thumbnail = serializers.Field(source='thumbnail')
    url = LessonHyperlinkedIdentityField(
        view_name='lesson',
        lookup_field='slug'
    )
    is_course_last_lesson = serializers.BooleanField(
        source='is_course_last_lesson',
        read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'course', 'is_course_last_lesson', 'desc',
                  'name', 'notes', 'position', 'slug', 'status', 'units', 'url',
                  'thumbnail')


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


class ClassSerializer(serializers.ModelSerializer):
    students = TimtecUserAdminCertificateSerializer(read_only=True)
    processes = CertificationProcessSerializer(read_only=True)

    class Meta:
        model = Class


class CourseProfessorSerializer(serializers.ModelSerializer):
    user_info = TimtecUserSerializer(source='user', read_only=True)
    course_info = CourseSerializer(source='course', read_only=True)
    get_name = serializers.Field()
    get_biography = serializers.Field()
    get_picture_url = serializers.Field()
    current_user_classes = ClassSerializer(source='get_current_user_classes', read_only=True)

    class Meta:
        fields = ('id', 'course', 'course_info', 'user', 'name', 'biography', 'picture', 'user_info',
                  'get_name', 'get_biography', 'get_picture_url', 'role', 'current_user_classes',
                  'is_course_author',)
        model = CourseProfessor


class CourseAuthorSerializer(serializers.ModelSerializer):
    user_info = TimtecUserSerializer(source='user', read_only=True)
    course_info = CourseSerializer(source='course', read_only=True)
    get_name = serializers.Field()
    get_biography = serializers.Field()
    get_picture_url = serializers.Field()

    class Meta:
        fields = ('id', 'course', 'course_info', 'user', 'name', 'biography', 'picture', 'user_info',
                  'get_name', 'get_biography', 'get_picture_url', 'position')
        model = CourseAuthor


class CourseAuthorPictureSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'picture',)
        model = CourseAuthor


class FlatpageSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlatPage
