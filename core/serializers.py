from core.models import Course, CourseProfessor, CourseStudent, TimtecUser
from rest_framework import serializers



class TimtecUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimtecUser
        fields = ('id', 'username', 'first_name', 'last_name',)


class CourseProfessorSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer()
    class Meta:
        model = CourseProfessor


class CourseStudentSerializer(serializers.ModelSerializer):
    user = TimtecUserSerializer()
    class Meta:
        model = CourseStudent


class CourseSerializer(serializers.ModelSerializer):
    courseprofessor_set = CourseProfessorSerializer(many=True)
    coursestudent_set = CourseStudentSerializer(many=True)

    class Meta:
        model = Course
        fields = ("id", "slug", "name", "intro_video", "application", "requirement",
                  "abstract", "structure", "workload", "pronatec", "status", "publication",
                  "courseprofessor_set", "coursestudent_set",)