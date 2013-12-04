# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.base import RedirectView, View, TemplateView
from django.contrib.contenttypes.models import ContentType
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from braces.views import LoginRequiredMixin
from notes.models import Note

from .serializers import CourseSerializer, LessonSerializer, StudentProgressSerializer, NoteUnitSerializer
from .models import Course, Lesson, StudentProgress, Unit

from forms import ContactForm


class HomeView(View):
    def get(self, request):
        latest = Course.objects.latest('publication')
        return redirect(reverse('course_intro', args=[latest.slug]))


class ContactView(View):
    def post(self, request):
        status_code = 200
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact_form.send_email()
            content = json.dumps([])
        else:
            status_code = 400
            content = json.dumps(contact_form.errors)

        response = self.options(request)
        response['Content-Type'] = 'application/json'
        response['Content-Length'] = len(content)
        response.content = content
        response.status_code = status_code

        return response


class CourseView(DetailView):
    model = Course
    template_name = 'course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated():
            units_done = StudentProgress.objects.filter(user=user, unit__lesson__course=self.object)\
                                                .exclude(complete=None)\
                                                .values_list('unit', flat=True)
            context['units_done'] = units_done

            user_is_enrolled = self.object.students.filter(id=user.id).exists()
            context['user_is_enrolled'] = user_is_enrolled

        return context


class UserCoursesView(LoginRequiredMixin, TemplateView):
    template_name = 'user-courses.html'


class EnrollCourseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        self.object = Course.objects.get(**self.kwargs)
        return self.object

    def get_redirect_url(self, **kwargs):
        course = self.get_object()
        course.enroll_student(self.request.user)
        return reverse('lesson', args=[course.first_lesson().slug])


class CourseViewSet(viewsets.ModelViewSet):
    model = Course
    lookup_field = 'slug'
    serializer_class = CourseSerializer

    def get(self, request, **kwargs):
        response = super(CourseViewSet, self).get(request, **kwargs)
        response['Cache-Control'] = 'no-cache'
        return response

    def post(self, request, **kwargs):
        course = self.get_object()
        serializer = CourseSerializer(course, request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=403)


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson.html"

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        unit_content_type = ContentType.objects.get_for_model(Unit)
        context['unit_content_type_id'] = unit_content_type.id
        return context


class LessonViewSet(viewsets.ModelViewSet):
    model = Lesson
    serializer_class = LessonSerializer
    filter_fields = ('course__slug',)

    def get_queryset(self):
        queryset = super(LessonViewSet, self).get_queryset()
        if self.request.user.is_active:
            return queryset
        return queryset.filter(published=True)


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
    model = StudentProgress

    def post(self, request, unitId=None):
        user = request.user

        try:
            unit = Unit.objects.get(id=unitId)
        except Unit.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = {}
        progress, created = StudentProgress.objects.get_or_create(user=user, unit=unit)
        progress.complete = timezone.now()
        progress.save()
        response['msg'] = 'Unit completed.'
        response['complete'] = progress.complete
        return Response(response, status=status.HTTP_201_CREATED)


class LessonsUserNotesViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    model = Lesson
    serializer_class = NoteUnitSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)
