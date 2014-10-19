# -*- coding: utf-8 -*-
from rest_framework import serializers
from core.models import CourseStudent, Course


class UserCourseStatsSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField('get_full_name')
    username = serializers.SerializerMethodField('get_username')
    email = serializers.SerializerMethodField('get_email')
    user_id = serializers.SerializerMethodField('get_user_id')
    course_progress = serializers.SerializerMethodField('get_user_progress')
    # forum_questions = serializers.SerializerMethodField('get_forum_questions')
    # forum_answers = serializers.SerializerMethodField('get_forum_answers')
#     lessons_stats = LessonUserStatsSerializer(many=True, allow_add_remove=False)

    class Meta:
        model = CourseStudent
        fields = ('name', 'username', 'email', 'user_id', 'course_progress',)

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_user_id(self, obj):
        return obj.user.id

    def get_user_progress(self, obj):
        return obj.percent_progress()

    # def get_forum_questions(self, obj):
    #     return obj.forum_questions_by_lesson()
    #
    # def get_forum_answers(self, obj):
    #     return obj.forum_answers_by_lesson()


class LessonUserStats(serializers.ModelSerializer):

    lessons_progress = serializers.SerializerMethodField('get_lessons_progress')
    forum_questions = serializers.SerializerMethodField('get_forum_questions')
    forum_answers = serializers.SerializerMethodField('get_forum_answers')

    class Meta:
        model = CourseStudent
        fields = ('lessons_progress',)

    @staticmethod
    def get_lessons_progress(obj):
        return obj.percent_progress_by_lesson()

    @staticmethod
    def get_forum_questions(obj):
        return obj.forum_questions_by_lesson()

    @staticmethod
    def get_forum_answers(obj):
        return obj.forum_answers_by_lesson()


class CourseStats(serializers.ModelSerializer):
    lessons_avg_progress = serializers.SerializerMethodField('get_lessons_avg_progress')
    # forum_answers = serializers.SerializerMethodField('get_forum_answers')

    class Meta:
        model = Course
        fields = ('slug', 'name', 'lessons_avg_progress',)

    @staticmethod
    def get_lessons_avg_progress(obj):
        if hasattr(obj, 'classes') and obj.classes:
            return obj.avg_lessons_users_progress(obj.classes)
        else:
            return obj.avg_lessons_users_progress()

    # @staticmethod
    # def get_forum_answers(obj):
    #     return obj.forum_answers_by_lesson()
