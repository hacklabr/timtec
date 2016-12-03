from .models import Activity, Answer
from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):

    data = serializers.JSONField()
    expected = serializers.JSONField(required=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('id', 'comment', 'data', 'expected', 'type', 'unit', 'image_url', 'positive_feedback', 'negative_feedback')

    @staticmethod
    def get_image_url(obj):
        if obj.image:
            return obj.image.url
            return ''


class AnswerSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    correct = serializers.ReadOnlyField(source='is_correct')
    given = serializers.JSONField()
    positive_feedback = serializers.ReadOnlyField(source='activity.positive_feedback')
    negative_feedback = serializers.ReadOnlyField(source='activity.negative_feedback')

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'user_id', 'timestamp',
                  'given', 'positive_feedback', 'negative_feedback')


class ActivityImportExportSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()
    expected = serializers.JSONField(required=False)

    class Meta:
        model = Activity
        exclude = ('id', 'unit',)
