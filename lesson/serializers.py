import json
from core.models import Activity, Lesson, StudentProgress, Unit, Video
from rest_framework import serializers


class JSONSerializerField(serializers.WritableField):

    def to_native(self, data):
        if type(data) is dict:
            return data
        elif type(data) in (unicode, str,):
            return json.loads(data)
        return None

    def from_native(self, obj):
        return json.dumps(obj)


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
        fields = ('id', 'video', 'activity', 'position',)


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    units = UnitSerializer(many=True, allow_add_remove=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='lesson',
        lookup_field='slug'
    )

    class Meta:
        model = Lesson
        fields = ('id', 'course', 'slug', 'desc', 'notes', 'name', 'url', 'units',)
