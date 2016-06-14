from forum.models import Question, Answer, QuestionVote, AnswerVote
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField('count_votes')
    username = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(read_only=True)
    hidden_to_user = serializers.SerializerMethodField('is_hidden')
    moderator = serializers.SerializerMethodField('is_moderator')

    class Meta:
        model = Question
        fields = ('id', 'title', 'course', 'answers', 'text', 'slug',
                  'votes', 'timestamp', 'username', 'hidden',
                  'hidden_by', 'hidden_to_user', 'moderator', 'hidden_justification',)

    def count_votes(self, obj):
        if obj:
            return obj.count_votes
        else:
            return 0

    def get_username(self, obj):
        if obj:
            return obj.user.username
        else:
            return u''

    def is_hidden(self, obj):
        if hasattr(obj, 'hidden_to_user'):
            return obj.hidden_to_user
        return obj.hidden

    def is_moderator(self, obj):
        if hasattr(obj, 'moderator'):
            return obj.moderator
        return False


class AnswerSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField('count_votes')
    username = serializers.SerializerMethodField('get_username')
    timestamp = serializers.DateTimeField(read_only=True)
    current_user_vote = serializers.SerializerMethodField('get_current_user_vote')

    class Meta:
        model = Answer
        fields = ('id', 'question', 'text', 'votes', 'timestamp', 'username', 'current_user_vote')

    def count_votes(self, obj):
        if obj:
            return obj.count_votes
        else:
            return 0

    def get_username(self, obj):
        if obj:
            return obj.user.username
        else:
            return u''

    def get_current_user_vote(self, obj):
        current_user_vote, _ = AnswerVote.objects.get_or_create(user=self.context.get('request').user, answer=obj)
        serializer = AnswerVoteSerializer(instance=current_user_vote, many=False, context=self.context)
        return serializer.data


class QuestionVoteSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = QuestionVote
        fields = ('question', 'timestamp', 'user', 'value')


class AnswerVoteSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AnswerVote
        fields = ('id', 'answer', 'timestamp', 'user', 'value')
