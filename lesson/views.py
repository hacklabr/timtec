# -*- coding: utf-8 -*-
import json
from datetime import datetime
from accounts.utils import LoginRequiredMixin
from core.models import Answer, Lesson, StudentProgress, Unit
from django.views.generic import DetailView
from lesson.serializers import LessonSerializer, StudentProgressSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson.html"


class LessonViewSet(viewsets.ModelViewSet):
    model = Lesson
    serializer_class = LessonSerializer
    filter_fields = ('course__slug',)


class StudentProgressViewSet(viewsets.ModelViewSet):
    model = StudentProgress
    serializer_class = StudentProgressSerializer
    filter_fields = ('unit__lesson',)

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(StudentProgressViewSet, self).pre_save(obj)

    def get_queryset(self):
        user = self.request.user
        return StudentProgress.objects.filter(user=user)


class UpdateStudentProgressView(APIView):
    model = Unit

    def post(self, request, unitId=None):
        user = request.user

        try:
            unit = Unit.objects.get(id=unitId)
        except Unit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = {}
        if not unit.activity:
            progress, created = StudentProgress.objects.get_or_create(user=user, unit=unit,
                                                                      complete=datetime.now())
            if created:
                response['msg'] = 'Unit completed.'
                response['complete'] = progress.complete
        return Response(response, status=status.HTTP_201_CREATED)


class ReceiveAnswerView(APIView):
    model = Unit

    def post(self, request, unitId=None):
        user = request.user
        unitId = int(unitId)

        try:
            unit = Unit.objects.get(id=unitId)
        except Unit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if 'given' in request.POST:
            answer = Answer(activity=unit.activity, user=user)
            answer.given = json.loads(request.POST.get('given', None))
            answer.save()

            progress, created = StudentProgress.objects.get_or_create(user=user, unit=unit)
            if answer.is_correct():
                progress.complete = datetime.now()
            progress.save()

            json_answer = {
                'expected': answer.expected,
                'given': answer.given,
                'correct': answer.is_correct(),
                'complete': progress.complete
            }

            return Response(json_answer, status=status.HTTP_201_CREATED)

        return Response({'error': 'Error receiving the Answer'}, status=status.HTTP_400_BAD_REQUEST)
