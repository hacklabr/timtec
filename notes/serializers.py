from notes.models import Note
from rest_framework import serializers
from core.serializers import UnitSerializer


class NoteSerializer(serializers.ModelSerializer):

    content_object = UnitSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'text', 'content_type', 'object_id', 'content_object')
