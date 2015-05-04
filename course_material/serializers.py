from course_material.models import CourseMaterial, File
from rest_framework import serializers


class FilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = File


class CourseMaterialSerializer(serializers.ModelSerializer):
    files = FilesSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = CourseMaterial


class CourseMaterialImportExportSerializer(serializers.ModelSerializer):
    files = FilesSerializer(many=True, required=False)

    class Meta:
        model = CourseMaterial
        fields = ('text', 'files',)
