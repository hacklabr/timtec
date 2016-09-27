from discussion.models import Topic
from discussion.serializers import TopicSerializer
from .models import Activity, Answer
from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):

    data = serializers.JSONField()
    expected = serializers.JSONField(required=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ('id', 'comment', 'data', 'expected', 'type', 'unit', 'image_url')

    @staticmethod
    def get_image_url(obj):
        if obj.image:
            return obj.image.url
        return ''


class ActivityImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'image')


class AnswerSerializer(serializers.ModelSerializer):
    correct = serializers.ReadOnlyField(source='is_correct')
    given = serializers.JSONField()
    topic = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        allow_add_remove = True
        fields = ('id', 'activity', 'correct', 'timestamp', 'given', 'topic')

    def get_topic(self, obj):
        try:
            topic = Topic.objects.get(id=obj.given['topic'])
        except Topic.DoesNotExist:
            return

        return TopicSerializer(instance=topic, **{'context': self.context}).data


class ActivityImportExportSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()
    expected = serializers.JSONField(required=False)

    class Meta:
        model = Activity
        exclude = ('id', 'unit',)
