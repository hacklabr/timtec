from .models import Activity, Answer
from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):

    data = serializers.JSONField('data')
    expected = serializers.JSONField('expected', required=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('id', 'comment', 'data', 'expected', 'type', 'unit', 'image_url')

    @staticmethod
    def get_image_url(obj):
        if obj.image:
            return obj.image.url
        return ''


class AnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    correct = serializers.ReadOnlyField(source='is_correct')
    given = serializers.JSONField('given')

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'user', 'user_id', 'timestamp', 'given',)


class ActivityImportExportSerializer(serializers.ModelSerializer):
    data = serializers.JSONField('data')
    expected = serializers.JSONField('expected', required=False)

    class Meta:
        model = Activity
        exclude = ('id', 'unit',)
