from .models import Activity, Answer
from rest_framework import serializers


class JSONSerializerField(serializers.WritableField):
    pass


class ActivitySerializer(serializers.ModelSerializer):
    data = JSONSerializerField('data')
    expected = JSONSerializerField('expected', required=False)

    class Meta:
        model = Activity
        fields = ('id', 'comment', 'data', 'expected', 'type', 'unit', )


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user')
    user_id = serializers.Field(source='user.id')
    correct = serializers.Field(source='is_correct')
    given = JSONSerializerField('given')

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'user', 'user_id', 'timestamp', 'given',)
