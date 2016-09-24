from django.contrib.flatpages.models import FlatPage
from django.contrib.auth import get_user_model
from core.models import (Course, CourseProfessor, CourseStudent, Lesson,
                         Video, StudentProgress, Unit, ProfessorMessage,
                         Class, CourseAuthor, CourseCertification,
                         CertificationProcess, Evaluation, CertificateTemplate,
                         IfCertificateTemplate)
from accounts.serializers import TimtecUserSerializer, \
    TimtecUserAdminCertificateSerializer
from activities.models import Activity, Answer
from activities.serializers import ActivitySerializer, AnswerSerializer
from notes.models import Note
from rest_framework import serializers


class ProfessorMessageSerializer(serializers.ModelSerializer):

    professor = TimtecUserSerializer(read_only=True)
    users_details = TimtecUserSerializer(source='users', read_only=True)

    class Meta:
        model = ProfessorMessage
        fields = ('id', 'course', 'users', 'subject', 'message', 'date', 'users_details',)


class BaseCourseSerializer(serializers.ModelSerializer):
    professors = serializers.SerializerMethodField('get_professor_name')
    home_thumbnail_url = serializers.SerializerMethodField()
    is_assistant_or_coordinator = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "status", "home_thumbnail_url",
                  "start_date", "home_published", "has_started",
                  "min_percent_to_complete", "professors", "is_assistant_or_coordinator",)

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

    def get_is_assistant_or_coordinator(self, obj):
        if self.context:
            return obj.is_assistant_or_coordinator(self.context['request'].user)


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


class ClassActivitySerializer(serializers.ModelSerializer):
    activity_answers = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['id', 'activity_answers', 'course']

    def get_activity_answers(self, obj):
        request = self.context.get("request")
        activity_id = request.query_params.get('activity', None)

        try:
            queryset = Answer.objects.filter(
                activity=activity_id,
                activity__unit__lesson__course=obj.course,
                user__in=obj.students.all()
            ).exclude(user=request.user)
        except Answer.DoesNotExist:
            return

        return AnswerSerializer(
            queryset, many=True, **{'context': self.context}).data


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id', 'name', 'youtube_id',)


class CourseSerializer(serializers.ModelSerializer):
    intro_video = VideoSerializer(required=False)
    home_thumbnail_url = serializers.SerializerMethodField()
    is_user_assistant = serializers.SerializerMethodField()
    is_user_coordinator = serializers.SerializerMethodField()
    is_assistant_or_coordinator = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status",
                  "thumbnail_url", "home_thumbnail_url", "home_position",
                  "start_date", "home_published", "authors_names", "has_started",
                  "min_percent_to_complete", "is_user_assistant", "is_user_coordinator",
                  "is_assistant_or_coordinator", )

    @staticmethod
    def get_home_thumbnail_url(obj):
        if obj.home_thumbnail:
            return obj.home_thumbnail.url
        return ''

    def get_is_user_assistant(self, obj):
        return obj.is_course_assistant(self.context['request'].user)

    def get_is_user_coordinator(self, obj):
        return obj.is_course_coordinator(self.context['request'].user)

    def get_is_assistant_or_coordinator(self, obj):
        return obj.is_assistant_or_coordinator(self.context['request'].user)


class CourseStudentSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer(read_only=True)

    current_class = BaseClassSerializer(source='get_current_class')
    course = BaseCourseSerializer()
    certificate = CourseCertificationSerializer()

    class Meta:
        model = CourseStudent
        fields = ('id', 'user', 'course', 'course_finished', 'course',
                  'certificate', 'can_emmit_receipt', 'percent_progress',
                  'current_class', 'min_percent_to_complete', 'start_date',)


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
    user = TimtecUserSerializer(read_only=True, required=False)

    class Meta:
        model = StudentProgress
        fields = ('unit', 'complete', 'user',)


class UnitSerializer(serializers.ModelSerializer):
    video = VideoSerializer(required=False, allow_null=True)
    activities = ActivitySerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Unit
        fields = ('id', 'title', 'video', 'activities', 'side_notes', 'position',)


class LessonSerializer(serializers.ModelSerializer):

    units = UnitSerializer(many=True)
    is_course_last_lesson = serializers.BooleanField(read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'course', 'is_course_last_lesson', 'desc',
                  'name', 'notes', 'position', 'slug', 'status', 'units',
                  'thumbnail')

    def update(self, instance, validated_data):

        units = self.update_units(self.initial_data.get('units'), instance)

        for old_unit in instance.units.all():
            if old_unit not in units:
                old_unit.delete()
            else:
                new_activities = units[units.index(old_unit)].activities
                if old_unit.activities != new_activities:
                    for activity in old_unit.activities:
                        if activity not in new_activities:
                            activity.delete()

        validated_data.pop('units')
        return super(LessonSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        units_data = validated_data.pop('units')
        new_lesson = super(LessonSerializer, self).create(validated_data)
        # units_data = self.initial_data.get('units')

        self.update_units(units_data, new_lesson)

        return new_lesson

    @classmethod
    def update_units(cls, units_data, lesson):
        units = []
        for unit_data in units_data:
            activities_data = unit_data.pop('activities')
            unit_data.pop('lesson', None)

            video_data = unit_data.pop('video', None)
            if video_data:
                video = Video(**video_data)
                video.save()
            else:
                video = None
            unit = Unit(lesson=lesson, video=video, **unit_data)
            unit.save()
            activities = []
            for activity_data in activities_data:
                # import pdb;pdb.set_trace()
                activity_id = activity_data.pop('id', None)
                activity, _ = Activity.objects.get_or_create(id=activity_id)
                activity.comment = activity_data.get('comment', None)
                activity.data = activity_data.get('data', None)
                activity.expected = activity_data.get('expected', None)
                activity.type = activity_data.get('type', None)
                activity.unit = unit
                activity.save()
                activities.append(activity)
            unit.activities = activities
            units.append(unit)
        return units


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

    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), required=False)
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
