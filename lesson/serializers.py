from core.models import Activity, Answer, Lesson, StudentProgress, Unit, Video
from rest_framework import serializers


class JSONSerializerField(serializers.WritableField):
    pass


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user')
    correct = serializers.Field(source='is_correct')
    given = JSONSerializerField('given')

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'user', 'timestamp', 'given',)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'name', 'youtube_id')


class ActivitySerializer(serializers.ModelSerializer):
    data = JSONSerializerField('data')
    expected = JSONSerializerField('expected')

    class Meta:
        model = Activity
        fields = ('id', 'type', 'data', 'expected',)


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
        fields = ('id', 'title', 'video', 'activity', 'position',)


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
