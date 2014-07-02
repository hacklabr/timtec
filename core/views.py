# -*- coding: utf-8 -*-
import json
import time

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.base import RedirectView, View, TemplateView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from braces.views import LoginRequiredMixin
from notes.models import Note

from .serializers import (CourseSerializer, CourseProfessorSerializer,
                          CourseThumbSerializer, LessonSerializer,
                          StudentProgressSerializer, CourseNoteSerializer,
                          LessonNoteSerializer, ProfessorMessageSerializer,
                          CourseStudentSerializer,)

from .models import Course, CourseProfessor, Lesson, StudentProgress, Unit, ProfessorMessage, CourseStudent

from .forms import ContactForm, AcceptTermsForm


class HomeView(ListView):
    context_object_name = 'courses'
    template_name = "home.html"

    def get_queryset(self):
        return Course.objects.all()

if settings.TWITTER_USER != '':
    from twitter import Twitter, OAuth

    class TwitterApi(View):

        def get(self, request, *args, **kwargs):

            consumer_key = settings.TWITTER_CONSUMER_KEY
            consumer_secret = settings.TWITTER_CONSUMER_SECRET
            twitter_name = settings.TWITTER_USER
            access_token = settings.TWITTER_ACESS_TOKEN
            access_token_secret = settings.TWITTER_ACESS_TOKEN_SECRET
            t = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))
            # To see all field returned, see https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline
            response = []
            for twit in t.statuses.user_timeline(screen_name=twitter_name, count=5):
                clean_twit = {}
                # time string example: Wed Aug 29 17:12:58 +0000 2012
                timestamp = time.strptime(twit['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
                clean_twit['date'] = time.strftime('%d/%m/%Y', timestamp)
                clean_twit['hour'] = time.strftime('%H:%M', timestamp)
                clean_twit['user_name'] = twit['user']['name']
                clean_twit['screen_name'] = twit['user']['screen_name']
                clean_twit['profile_image_url'] = twit['user']['profile_image_url']
                clean_twit['text'] = twit['text']
                response.append(clean_twit)

            response = json.dumps(response)
            return HttpResponse(
                response,
                content_type='application/json'
            )


class CoursesView(ListView):
    context_object_name = 'courses'
    template_name = "courses.html"

    def get_queryset(self):
        return Course.objects.all().prefetch_related('professors')


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
        if self.request.user.accepted_terms:
            course.enroll_student(self.request.user)
            return reverse_lazy('lesson', args=[course.slug, course.first_lesson().slug])
        else:
            return reverse_lazy('accept_terms')


class AcceptTermsView(FormView):
    template_name = 'accept-terms.html'
    form_class = AcceptTermsForm
    success_url = reverse_lazy('courses')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.request.user.accepted_terms = True
        self.request.user.save()
        return super(AcceptTermsView, self).form_valid(form)


class CourseProfessorViewSet(viewsets.ModelViewSet):
    model = CourseProfessor
    lookup_field = 'id'
    filter_fields = ('course', 'user',)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CourseProfessorSerializer


class CourseStudentViewSet(viewsets.ModelViewSet):
    model = CourseStudent
    lookup_field = 'id'
    filter_fields = ('course', 'user',)
#     filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CourseStudentSerializer


class ProfessorMessageViewSet(viewsets.ModelViewSet):
    model = ProfessorMessage
    lookup_field = 'id'
    filter_fields = ('course',)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = ProfessorMessageSerializer

    def pre_save(self, obj):
        obj.professor = self.request.user
        return super(ProfessorMessageViewSet, self).pre_save(obj)

    def post_save(self, obj, created):
        if created:
            obj.send()


class CourseViewSet(viewsets.ModelViewSet):
    model = Course
    lookup_field = 'id'
    filter_fields = ('slug', 'home_published',)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
            return Response(serializer.errors, status=400)

    def metadata(self, request):
        data = super(CourseViewSet, self).metadata(request)
        data.get('actions').get('POST').get('status').update({'choices': dict(Course.STATES[1:])})
        return data


class CourseThumbViewSet(viewsets.ModelViewSet):
    model = Course
    lookup_field = 'id'
    serializer_class = CourseThumbSerializer

    def post(self, request, **kwargs):
        course = self.get_object()
        serializer = CourseThumbSerializer(course, request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "lesson.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(LessonDetailView, self).get_queryset(*args, **kwargs)
        course_slug = self.kwargs.get('course_slug')
        return qs.filter(course__slug=course_slug)

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        unit_content_type = ContentType.objects.get_for_model(Unit)
        context['unit_content_type_id'] = unit_content_type.id
        return context


class LessonViewSet(viewsets.ModelViewSet):
    model = Lesson
    serializer_class = LessonSerializer
    filter_fields = ('course__slug', 'course__id',)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    ordering = ('position',)

    def get_queryset(self):
        queryset = super(LessonViewSet, self).get_queryset()
        if self.request.user.is_active:
            return queryset
        return queryset.filter(published=True)


class StudentProgressViewSet(viewsets.ModelViewSet):
    model = StudentProgress
    serializer_class = StudentProgressSerializer
    filter_fields = ('unit', 'unit__lesson',)

    def pre_save(self, obj):
        obj.user = self.request.user
        return super(StudentProgressViewSet, self).pre_save(obj)

    def get_queryset(self):
        user = self.request.user
        return StudentProgress.objects.filter(user=user)


class UserNotesViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    model = Course
    lookup_field = 'course'

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        if 'course' in self.kwargs:
            course = get_object_or_404(Course, slug=self.kwargs['course'])
            units = Unit.objects.filter(lesson__course=course, notes__user=user).exclude(notes__isnull=True)

            lessons_dict = {}
            for unit in units:
                lesson = unit.lesson
                if lesson.slug not in lessons_dict:
                    lessons_dict[lesson.slug] = lesson
                    lessons_dict[lesson.slug].units_notes = []
                unit_type = ContentType.objects.get_for_model(unit)
                note = get_object_or_404(Note, user=user, content_type__pk=unit_type.id, object_id=unit.id)
                unit.user_note = note
                lessons_dict[lesson.slug].units_notes.append(unit)

            results = []
            for lesson in lessons_dict.values():
                results.append(LessonNoteSerializer(lesson).data)
            return Response(results)

    def list(self, request, *args, **kwargs):
        user = self.request.user
        units = Unit.objects.filter(notes__user=user).exclude(notes__isnull=True)
        courses = {}
        for unit in units:
            course = unit.lesson.course
            lesson = unit.lesson
            if course.slug not in courses:
                courses[course.slug] = course
                courses[course.slug].lessons_dict = {}
            if lesson.slug not\
                    in courses[course.slug].lessons_dict:
                courses[course.slug].lessons_dict[lesson.slug] = lesson
                courses[course.slug].lessons_dict[lesson.slug].units_notes = []
#             unit_type = ContentType.objects.get_for_model(unit)
#             note = get_object_or_404(Note, user=user, content_type__pk=unit_type.id, object_id=unit.id)
#             unit.user_note = note
#             courses[course.slug].lessons_dict[lesson.slug].units_notes.append(unit)

        results = []
        for course in courses.values():
            course.lessons_notes = course.lessons_dict.values()
            course.course_notes_number = Unit.objects.filter(lesson__course=course, notes__user=user).exclude(notes__isnull=True).count()
            del course.lessons_dict
            results.append(CourseNoteSerializer(course).data)
        return Response(results)
