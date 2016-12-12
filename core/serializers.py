from django.contrib.flatpages.models import FlatPage
from django.contrib.auth import get_user_model
from core.models import (Course, CourseProfessor, CourseStudent, Lesson,
                         Video, StudentProgress, Unit, ProfessorMessage,
                         Class, CourseAuthor, CourseCertification,
                         CertificationProcess, Evaluation, CertificateTemplate,
                         IfCertificateTemplate)
from accounts.serializers import (TimtecUserSerializer,
                                  TimtecUserAdminCertificateSerializer, TimtecUserAdminSerializer)
from activities.serializers import ActivitySerializer
from rest_framework.reverse import reverse_lazy
from notes.models import Note
from rest_framework import serializers
from accounts.models import UserSocialAccount


class ProfessorMessageSerializer(serializers.ModelSerializer):

    professor = TimtecUserSerializer(source='professor', read_only=True)
    # users_details = TimtecUserSerializer(source='users', read_only=True)
    users = serializers.PrimaryKeyRelatedField(source='users', write_only=True, many=True)

    class Meta:
        model = ProfessorMessage
        fields = ('id', 'users', 'course', 'subject', 'message', 'date',)


class ProfessorMessageUserDetailsSerializer(serializers.ModelSerializer):

    professor = TimtecUserSerializer(source='professor', read_only=True)
    users_details = TimtecUserAdminSerializer(source='users', read_only=True)

    class Meta:
        model = ProfessorMessage
        fields = ('id', 'course', 'users', 'subject', 'message', 'date', 'users_details', 'professor')


class BaseCourseSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.Field(source='get_thumbnail_url')
    has_started = serializers.Field()
    professors = serializers.SerializerMethodField('get_professor_name')
    home_thumbnail_url = serializers.SerializerMethodField('get_home_thumbnail_url')

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
    course_certification = serializers.SlugRelatedField(slug_field="link_hash")

    class Meta:
        model = CertificationProcess


class CourseCertificationSerializer(serializers.ModelSerializer):
    processes = BaseCertificationProcessSerializer(many=True, read_only=True)
    approved = BaseCertificationProcessSerializer(source='get_approved_process', read_only=True)
    course = serializers.SerializerMethodField('get_course')
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = CourseCertification
        fields = ('link_hash', 'created_date', 'is_valid', 'processes', 'type',
                  'approved', 'course', 'url')

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
    professors = TimtecUserSerializer(source="professors", read_only=True)

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status",
                  "thumbnail_url", "home_thumbnail_url", "home_position",
                  "start_date", "professor_name", "home_published",
                  "professors_names", "has_started", 'professors',
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


class CourseStudentSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer(read_only=True)

    course_finished = serializers.BooleanField(source='course_finished')
    can_emmit_receipt = serializers.BooleanField(source='can_emmit_receipt')
    percent_progress = serializers.IntegerField(source='percent_progress')
    min_percent_to_complete = serializers.IntegerField(
        source='min_percent_to_complete')

    current_class = BaseClassSerializer(source='get_current_class')
    course = BaseCourseSerializer()
    certificate = CourseCertificationSerializer()

    class Meta:
        model = CourseStudent
        fields = ('id', 'user', 'course', 'course_finished',
                  'certificate', 'can_emmit_receipt', 'percent_progress',
                  'current_class', 'min_percent_to_complete',)


class CourseStudentClassSerializer(CourseStudentSerializer):

    user = TimtecUserAdminCertificateSerializer(read_only=True)

    class Meta:
        model = CourseStudent
        fields = ('id', 'user', 'course_finished',
                  'certificate', 'can_emmit_receipt', 'percent_progress',)


class ClassSerializer(serializers.ModelSerializer):
    students = CourseStudentClassSerializer(source='get_students', many=True, read_only=True)
    processes = CertificationProcessSerializer(read_only=True)
    evaluations = EvaluationSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    assistant = TimtecUserSerializer(read_only=True)
    students_management = serializers.PrimaryKeyRelatedField(many=True, read_only=False, source='students')
    assistant_management = serializers.PrimaryKeyRelatedField(read_only=False, source='assistant', required=False)

    class Meta:
        model = Class


class UserSocialAccountSerializer(serializers.ModelSerializer):

    get_absolute_url = serializers.Field()

    class Meta:
        model = UserSocialAccount
        fields = ('social_media', 'nickname', 'get_absolute_url')


class ProfileSerializer(TimtecUserSerializer):

    certificates = ProfileCourseCertificationSerializer(many=True, source="get_certificates")
    social_medias = UserSocialAccountSerializer(many=True, source='get_social_media')
    courses = BaseCourseSerializer(many=True, source='get_current_courses')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'biography', 'picture', 'is_profile_filled', 'occupation', 'birth_date',
                  'certificates', 'city', 'state', 'site', 'occupation', 'social_medias', 'courses')


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
        # fields = ('id', 'title', 'video', 'position')


class LessonNoteSerializer(serializers.ModelSerializer):

    units_notes = UnitNoteSerializer(many=True)
    course = serializers.SlugRelatedField(slug_field='slug')

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'position', 'slug', 'course', 'units_notes',)
        # fields = ('id', 'name', 'position', 'slug', 'course',)


class CourseNoteSerializer(serializers.ModelSerializer):

    lessons_notes = serializers.SerializerMethodField('get_lessons_notes')
    course_notes_number = serializers.IntegerField(required=False)

    def get_lessons_notes(self, obj):
        return [LessonNoteSerializer(item).data for item in obj.lessons_notes]

    class Meta:
        model = Course
        fields = ('id', 'slug', 'name', 'lessons_notes', 'course_notes_number',)


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
