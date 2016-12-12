from .models import Activity, Answer
from rest_framework import serializers


class JSONSerializerField(serializers.WritableField):
    pass


class ActivitySerializer(serializers.ModelSerializer):
    data = JSONSerializerField('data')
    expected = JSONSerializerField('expected', required=False)

    class Meta:
        model = Activity
        fields = ('id', 'comment', 'data', 'expected', 'type', 'unit', 'positive_feedback', 'negative_feedback')


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user')
    user_id = serializers.Field(source='user.id')
    correct = serializers.Field(source='is_correct')
    given = JSONSerializerField('given')
    positive_feedback = serializers.Field('activity.positive_feedback')
    negative_feedback = serializers.Field('activity.negative_feedback')

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'user', 'user_id', 'timestamp', 'given', 'positive_feedback', 'negative_feedback')


class ActivityImportExportSerializer(serializers.ModelSerializer):
    data = JSONSerializerField('data')
    expected = JSONSerializerField('expected', required=False)

    class Meta:
        model = Activity
        exclude = ('id', 'unit',)
