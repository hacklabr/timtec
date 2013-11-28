from notes.models import Note
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
