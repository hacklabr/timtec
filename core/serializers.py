from django.contrib.flatpages.models import FlatPage
from django.contrib.auth import get_user_model
from core.models import (Course, CourseProfessor, CourseStudent, Lesson,
                         Video, StudentProgress, Unit, ProfessorMessage,
                         Class, CourseAuthor, CourseCertification,
                         CertificationProcess, Evaluation, CertificateTemplate,
                         IfCertificateTemplate)
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


class BaseCourseSerializer(serializers.ModelSerializer):
    professors = serializers.SerializerMethodField('get_professor_name')
    home_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "status", "home_thumbnail_url",
                  "start_date", "home_published", "has_started",
                  "min_percent_to_complete", "professors")

    @staticmethod
    def get_professor_name(obj):
        if obj.course_authors.all():
            return [author.get_name() for author in obj.course_authors.all()]
        return ''

    @staticmethod
    def get_home_thumbnail_url(obj):
        if obj.home_thumbnail:
            return obj.home_thumbnail.url
        return ''


class BaseClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ("id", "name", "assistant", "user_can_certificate")


class BaseEvaluationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluation


class BaseCertificationProcessSerializer(serializers.ModelSerializer):
    evaluation = BaseEvaluationSerializer()

    class Meta:
        model = CertificationProcess


class BaseCourseCertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCertification


class CertificationProcessSerializer(serializers.ModelSerializer):
    # TODO: Verificar se de fato e read_only=True
    course_certification = serializers.SlugRelatedField(slug_field="link_hash", read_only=True)

    class Meta:
        model = CertificationProcess


class CourseCertificationSerializer(serializers.ModelSerializer):
    processes = BaseCertificationProcessSerializer(many=True, read_only=True)
    approved = BaseCertificationProcessSerializer(source='get_approved_process')
    course = serializers.SerializerMethodField()

    class Meta:
        model = CourseCertification
        fields = ('link_hash', 'created_date', 'is_valid', 'processes', 'type',
                  'approved', 'course')

    @staticmethod
    def get_course(obj):
        return obj.course.id


class ProfileCourseCertificationSerializer(serializers.ModelSerializer):
    course = BaseCourseSerializer()
    approved = BaseCertificationProcessSerializer(source='get_approved_process')

    class Meta:
        model = CourseCertification
        fields = ('link_hash', 'created_date', 'is_valid', 'processes', 'type',
                  'approved', 'course')


class EvaluationSerializer(serializers.ModelSerializer):
    processes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Evaluation


class CertificateTemplateSerializer(serializers.ModelSerializer):
    base_logo_url = serializers.Field(source='base_logo_url')
    cert_logo_url = serializers.Field(source='cert_logo_url')

    class Meta:
        model = CertificateTemplate
        fields = ('id', 'course', 'organization_name', 'base_logo_url', 'cert_logo_url', 'role', 'name',)


class IfCertificateTemplateSerializer(CertificateTemplateSerializer):

    class Meta:
        model = IfCertificateTemplate
        fields = ('id', 'course', 'organization_name', 'base_logo_url', 'cert_logo_url',
                  'pronatec_logo', 'mec_logo', 'role', 'name',)


class CertificateTemplateImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CertificateTemplate
        fields = ('base_logo', 'cert_logo', )


class ClassSerializer(serializers.ModelSerializer):
    students = TimtecUserAdminCertificateSerializer(read_only=True, many=True)
    processes = CertificationProcessSerializer(read_only=True, many=True)
    evaluations = EvaluationSerializer(read_only=True, many=True)

    class Meta:
        model = Class


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id', 'name', 'youtube_id',)


class CourseSerializer(serializers.ModelSerializer):
    intro_video = VideoSerializer(required=False)
    home_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status",
                  "thumbnail_url", "home_thumbnail_url", "home_position",
                  "start_date", "home_published", "authors_names", "has_started",
                  "min_percent_to_complete")

    @staticmethod
    def get_home_thumbnail_url(obj):
        if obj.home_thumbnail:
            return obj.home_thumbnail.url
        return ''


class CourseStudentSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer(read_only=True)

    current_class = BaseClassSerializer(source='get_current_class')
    course = BaseCourseSerializer()
    certificate = CourseCertificationSerializer()

    class Meta:
        model = CourseStudent
        fields = ('id', 'user', 'course', 'course_finished', 'course',
                  'certificate', 'can_emmit_receipt', 'percent_progress',
                  'current_class', 'min_percent_to_complete',)


class ProfileSerializer(TimtecUserSerializer):
    certificates = ProfileCourseCertificationSerializer(many=True,
                                                        source="get_certificates")

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'biography', 'picture', 'is_profile_filled', 'occupation',
                  'certificates', 'city', 'site', 'occupation', )


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
    activities = ActivitySerializer(many=True)

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
    # TODO: Verificar se de fato e read_only=True
    course = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    units = UnitSerializer(many=True)
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
        # fields = ('id', 'title', 'video', 'position')


class LessonNoteSerializer(serializers.ModelSerializer):

    units_notes = UnitNoteSerializer(many=True)
    course = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'position', 'slug', 'course', 'units_notes',)
        # fields = ('id', 'name', 'position', 'slug', 'course',)


class CourseNoteSerializer(serializers.ModelSerializer):

    lessons_notes = LessonNoteSerializer(many=True)
    course_notes_number = serializers.IntegerField(required=False)

    class Meta:
        model = Course
        fields = ('id', 'slug', 'name', 'lessons_notes', 'course_notes_number',)


class CourseProfessorSerializer(serializers.ModelSerializer):
    user_info = TimtecUserSerializer(source='user', read_only=True)
    course_info = CourseSerializer(source='course', read_only=True)
    get_name = serializers.CharField(read_only=True)
    get_biography = serializers.CharField(read_only=True)
    get_picture_url = serializers.CharField(read_only=True)
    current_user_classes = ClassSerializer(source='get_current_user_classes', read_only=True, many=True)

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
