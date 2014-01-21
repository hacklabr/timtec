from .models import Activity, Answer
from rest_framework import serializers


class JSONSerializerField(serializers.WritableField):
    pass


class ActivitySerializer(serializers.ModelSerializer):
    data = JSONSerializerField('data')
    expected = JSONSerializerField('expected')

    class Meta:
        model = Activity
        fields = ('id', 'type', 'data', 'expected',)


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user')
    correct = serializers.Field(source='is_correct')
    given = JSONSerializerField('given')

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'user', 'timestamp', 'given',)
