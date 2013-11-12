from course_material.models import CourseMaterial
from rest_framework import serializers


class CourseMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseMaterial
