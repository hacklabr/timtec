from forum.models import Question, Answer, QuestionVote, AnswerVote
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('title', 'text', 'slug')


class AnswerSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField('count_votes')
    username = serializers.SerializerMethodField('get_username')
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Answer
        fields = ('question', 'text', 'votes', 'timestamp', 'username')

    def count_votes(self, obj):
        if obj:
            return obj.votes.count()
        else:
            return 0

    def get_username(self, obj):
        if obj:
            return obj.user.username
        else:
            return u''


class QuestionVoteSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = QuestionVote
        fields = ('question', 'timestamp', 'user', 'value')


class AnswerVoteSerializer(serializers.ModelSerializer):

    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnswerVote
        fields = ('question', 'timestamp', 'user', 'value')
