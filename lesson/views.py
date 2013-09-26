# -*- coding: utf-8 -*-
import json
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


class ReceiveAnswerView(APIView):
    model = Unit

    def post(self, request, unitId=None):
        user = request.user
        unitId = int(unitId)

        try:
            unit = Unit.objects.get(id=unitId)
        except Unit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if 'choice' in request.POST:
            answer = {'choice': request.POST.get('choice', None)}

            instance = Answer(activity=unit.activity, user=user)
            instance.answer = json.dumps(answer)
            instance.save()

            answer['id'] = instance.id
            return Response(answer, status=status.HTTP_201_CREATED)