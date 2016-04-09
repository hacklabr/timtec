from .models import Activity, Answer
from rest_framework import serializers


class JSONSerializerField(serializers.WritableField):
    pass


class ActivitySerializer(serializers.ModelSerializer):
    data = JSONSerializerField('data')
    expected = JSONSerializerField('expected', required=False)
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Activity
        fields = ('id', 'comment', 'data', 'expected', 'type', 'unit', 'image_url')

    @staticmethod
    def get_image_url(obj):
        if obj.image:
            return obj.image.url
        return ''


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user')
    user_id = serializers.Field(source='user.id')
    correct = serializers.Field(source='is_correct')
    given = JSONSerializerField('given')

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'user', 'user_id', 'timestamp', 'given',)


class ActivityImportExportSerializer(serializers.ModelSerializer):
    data = JSONSerializerField('data')
    expected = JSONSerializerField('expected', required=False)

    class Meta:
        model = Activity
        exclude = ('id', 'unit',)
