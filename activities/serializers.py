from .models import Activity, Answer
from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):
    data = serializers.JSONField('data')
    expected = serializers.JSONField('expected', required=False)

    class Meta:
        model = Activity
        fields = ('id', 'comment', 'data', 'expected', 'type', 'unit', )


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user')
    user_id = serializers.Field(source='user.id')
    correct = serializers.Field(source='is_correct')
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
