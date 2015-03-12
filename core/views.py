# -*- coding: utf-8 -*-
import json
import time
import datetime

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic import (DetailView, ListView, DeleteView,
                                  CreateView, UpdateView)
from django.views.generic.base import RedirectView, View, TemplateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
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
                          CourseStudentSerializer, ClassSerializer,
                          FlatpageSerializer, CourseProfessorPictureSerializer)

from .models import (Course, CourseProfessor, Lesson, StudentProgress,
                     Unit, ProfessorMessage, CourseStudent, Class)

from .forms import (ContactForm, RemoveStudentForm,
                    AddStudentsForm, )

from .permissions import IsProfessorCoordinatorOrAdminPermissionOrReadOnly, IsAdminOrReadOnly


class HomeView(ListView):
    context_object_name = 'home_courses'
    template_name = "home.html"

    def get_queryset(self):
        return Course.objects.filter(home_published=True).order_by('home_position')

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
        return Course.objects.filter(Q(status='published') | Q(status='listed')).prefetch_related('professors').order_by('start_date')


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


class GenericCourseView(DetailView):
    model = Course
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'


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

    def get_context_data(self, **kwargs):
        context = super(UserCoursesView, self).get_context_data(**kwargs)

        context['courses_user_assist'] = CourseProfessor.objects.filter(user=self.request.user, role='assistant').exists()

        context['courses_user_coordinate'] = CourseProfessor.objects.filter(user=self.request.user, role='coordinator').exists()

        return context


class EnrollCourseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        self.object = Course.objects.get(**self.kwargs)
        return self.object

    def get_redirect_url(self, **kwargs):
        course = self.get_object()
        if course.is_enrolled(self.request.user):
            return reverse_lazy('resume_course', args=[course.slug])
        if self.request.user.accepted_terms or not settings.TERMS_ACCEPTANCE_REQUIRED:
            course.enroll_student(self.request.user)
            if course.has_started and course.first_lesson():
                return reverse_lazy('lesson', args=[course.slug, course.first_lesson().slug])
            else:
                return reverse_lazy('course_intro', args=[course.slug])
        else:
            return '{}?next={}'.format(reverse_lazy('accept_terms'), self.request.path)


class ResumeCourseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_object(self):
        if hasattr(self, 'object'):
            return self.object
        self.object = Course.objects.get(**self.kwargs)
        return self.object

    def get_redirect_url(self, **kwargs):
        course = self.get_object()
        if self.request.user.accepted_terms or not settings.TERMS_ACCEPTANCE_REQUIRED:
            course_student, _ = CourseStudent.objects.get_or_create(user=self.request.user, course=course)
            last_unit = course_student.resume_next_unit()
            url = reverse_lazy('lesson', args=[course.slug, last_unit.lesson.slug])
            return url + '#' + str(last_unit.position + 1)
        else:
            return reverse_lazy('accept_terms')


class CourseProfessorViewSet(viewsets.ModelViewSet):
    model = CourseProfessor
    lookup_field = 'id'
    filter_fields = ('course', 'user', 'role',)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CourseProfessorSerializer
    permission_classes = (IsProfessorCoordinatorOrAdminPermissionOrReadOnly, )

    def pre_save(self, obj):
        # Verify if current user is coordinator. The has_object_permission method is not called when creating objects,
        # so we call it explicitly here. See: https://github.com/tomchristie/django-rest-framework/issues/1103
        self.check_object_permissions(self.request, obj)
        return super(CourseProfessorViewSet, self).pre_save(obj)

    def get_queryset(self):
        queryset = super(CourseProfessorViewSet, self).get_queryset()
        has_user = self.request.QUERY_PARAMS.get('has_user', None)
        if has_user:
            queryset = queryset.exclude(user=None)
        return queryset


class CoursePictureUploadViewSet(viewsets.ModelViewSet):
    model = CourseProfessor
    lookup_field = 'id'
    serializer_class = CourseProfessorPictureSerializer

    def post(self, request, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)


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
    permission_classes = (IsProfessorCoordinatorOrAdminPermissionOrReadOnly,)

    def get_queryset(self):
        queryset = super(CourseViewSet, self).get_queryset()
        public_courses = self.request.QUERY_PARAMS.get('public_courses', None)
        if public_courses:
            queryset = queryset.filter(Q(status='published') | Q(status='listed')).prefetch_related('professors')
        return queryset

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
        if data.get('actions'):
            data.get('actions').get('POST').get('status').update({'choices': dict(Course.STATES[1:])})
        return data


class CourseThumbViewSet(viewsets.ModelViewSet):
    model = Course
    lookup_field = 'id'
    serializer_class = CourseThumbSerializer
    permission_classes = (IsProfessorCoordinatorOrAdminPermissionOrReadOnly, )

    def post(self, request, **kwargs):
        course = self.get_object()
        serializer = CourseThumbSerializer(course, request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)


class CarouselCourseView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    serializer_class = CourseSerializer
    filter_fields = ('slug', 'home_published',)
    queryset = Course.objects.exclude(status=Course.STATES[0][0]).exclude(status=Course.STATES[1][0]).filter(start_date__gte=datetime.date.today())
    permission_classes = (IsAuthenticatedOrReadOnly,)


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
        course = self.object.course
        lessons = list(course.public_lessons)
        if lessons and self.object != lessons[-1]:
            index = lessons.index(self.object)
            context['next_url'] = reverse_lazy('lesson',
                                               args=[course.slug,
                                                     lessons[index + 1].slug])
        context['unit_content_type_id'] = unit_content_type.id
        return context


class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'classes.html'

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs.get('course_slug'))
        self.course = course
        user = self.request.user
        queryset = course.class_set.all()

        if course.has_perm_own_all_classes(user):
            return queryset
        else:
            return queryset.filter(assistant=user)

    def get_context_data(self, **kwargs):
        context = super(ClassListView, self).get_context_data(**kwargs)
        context['course'] = self.course
        return context


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    # template_name = 'class_edit.html'
    fields = ('course', 'name', )

    def form_valid(self, form):
        form.instance.assistant = self.request.user
        return super(ClassCreateView, self).form_valid(form)


class CanEditClassMixin(object):
    def check_permission(self, klass):
        user = self.request.user
        if not (user == klass.assistant or klass.course.has_perm_own_all_classes(user)):
            raise PermissionDenied

    def get_object(self, queryset=None):
        klass = super(CanEditClassMixin, self).get_object(queryset=queryset)
        self.check_permission(klass)
        return klass


class ClassUpdateView(LoginRequiredMixin, CanEditClassMixin, UpdateView):
    model = Class
    template_name = 'class_edit.html'
    fields = ('name', 'assistant', )

    def get_context_data(self, **kwargs):
        context = super(ClassUpdateView, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        if form.changed_data:
            if 'assistant' in form.changed_data and not self.object.course.is_course_coordinator(self.request.user):
                raise PermissionDenied

        return super(ClassUpdateView, self).form_valid(form)


class ClassDeleteView(LoginRequiredMixin, CanEditClassMixin, DeleteView):
    model = Class
    template_name = 'base.html'
    http_method_names = ['post', ]

    def get_success_url(self):
        return reverse_lazy('classes', kwargs={'course_slug': self.object.course.slug})

    def get_object(self, queryset=None):
        klass = super(ClassDeleteView, self).get_object(queryset=queryset)

        if klass == klass.course.default_class:
            raise PermissionDenied

        return klass


class ClassRemoveUserView(LoginRequiredMixin, CanEditClassMixin, UpdateView):
    model = Class
    form_class = RemoveStudentForm
    http_method_names = ['post', ]

    def get_success_url(self):
        return reverse_lazy('class', kwargs={'pk': self.object.id})


class ClassAddUsersView(LoginRequiredMixin, CanEditClassMixin, UpdateView):
    model = Class
    form_class = AddStudentsForm
    http_method_names = ['post', ]

    def get_success_url(self):
        return reverse_lazy('class', kwargs={'pk': self.object.id})


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
    lookup_field = 'unit'

    def update(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        if self.object:
            self.object.save()
            return HttpResponse('')
        else:
            return super(StudentProgressViewSet, self).update(request, *args, **kwargs)

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.unit = Unit.objects.get(id=self.kwargs.get('unit'))
        obj.complete = timezone.now()
        return obj

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


class ClassViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):

    model = Class
    serializer_class = ClassSerializer
    filter_fields = ('course',)

    def get_queryset(self):
        queryset = super(ClassViewSet, self).get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset

        course_id = self.request.QUERY_PARAMS.get('course')
        if course_id:
            try:
                role = self.request.user.teaching_courses.get(course__id=course_id).role
            except ObjectDoesNotExist:
                role = ''
            # if user is not coordinator or admin, only show his classes
            if not role or role == 'assistant':
                queryset = queryset.filter(assistant=self.request.user)

        return queryset


class FlatpageViewSet(viewsets.ModelViewSet):

    model = FlatPage
    serializer_class = FlatpageSerializer
    filter_fields = ('url',)
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = super(FlatpageViewSet, self).get_queryset()
        url_prefix = self.request.QUERY_PARAMS.get('url_prefix')
        if url_prefix:
            queryset = queryset.filter(url__startswith=url_prefix)
        return queryset
