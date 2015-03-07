from course_material.models import CourseMaterial, File
from rest_framework import serializers


class CourseMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseMaterial


class FilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('file', 'course_material',)


class CourseMaterialImportExportSerializer(serializers.ModelSerializer):
    files = FilesSerializer(many=True, required=False)

    class Meta:
        model = CourseMaterial
        fields = ('text', 'files',)
