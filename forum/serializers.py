from forum.models import Question, Answer
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('title', 'text', 'slug')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('question', 'text',)
