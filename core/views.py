# -*- coding: utf-8 -*-
import json
import time
import datetime

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.views.generic import (DetailView, ListView, DeleteView,
                                  CreateView, UpdateView)
from django.views.generic.base import RedirectView, View, TemplateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
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
                          FlatpageSerializer, CourseAuthorPictureSerializer,
                          CourseAuthorSerializer,
                          CourseCertificationSerializer,
                          CertificationProcessSerializer,
                          EvaluationSerializer, ProfileSerializer, ProfessorMessageUserDetailsSerializer,
                          IfCertificateTemplateSerializer, CertificateTemplateImageSerializer)

from .models import (Course, CourseProfessor, Lesson, StudentProgress,
                     Unit, ProfessorMessage, CourseStudent, Class,
                     CourseAuthor, CourseCertification, CertificationProcess,
                     Evaluation, CertificateTemplate, IfCertificateTemplate)

from .forms import (ContactForm, RemoveStudentForm)

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
        return Course.objects.filter(status='published').prefetch_related('professors').order_by('start_date')


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


class GenericCourseView(LoginRequiredMixin, DetailView):
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

        context['courses_user_assist'] = CourseProfessor.objects.filter(
            user=self.request.user,
            role='assistant'
        ).exists()

        context['courses_user_coordinate'] = CourseProfessor.objects.filter(
            user=self.request.user,
            role='coordinator'
        ).exists()

        context['user_has_certificates'] = CourseCertification.objects.filter(
            course_student__user=self.request.user).exists()

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
        if course.status == 'draft':
            return reverse_lazy('courses')
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
            if not course.is_enrolled(self.request.user):
                course.enroll_student(self.request.user)
                return reverse_lazy('lesson', args=[course.slug, course.first_lesson().slug])
            course_student = self.request.user.coursestudent_set.get(course=course)
            last_unit = course_student.resume_next_unit()
            url = reverse_lazy('lesson', args=[course.slug, last_unit.lesson.slug])
            return url + '#' + str(last_unit.position + 1)
        else:
            return reverse_lazy('accept_terms')


class CourseProfessorViewSet(viewsets.ModelViewSet):
    model = CourseProfessor
    lookup_field = 'id'
    filter_fields = ('course', 'user', 'role', 'is_course_author',)
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
        is_course_author = self.request.QUERY_PARAMS.get('is_course_author', None)
        if is_course_author == 'true':
            queryset = queryset.filter(is_course_author=True)
        if is_course_author == 'false':
            queryset = queryset.filter(is_course_author=False)

        has_user = self.request.QUERY_PARAMS.get('has_user', None)
        if has_user:
            queryset = queryset.exclude(user=None)
        return queryset


class CourseAuthorViewSet(viewsets.ModelViewSet):
    model = CourseAuthor
    lookup_field = 'id'
    filter_fields = ('course', 'user',)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CourseAuthorSerializer
    permission_classes = (IsProfessorCoordinatorOrAdminPermissionOrReadOnly, )

    def pre_save(self, obj):
        # Verify if current user is coordinator. The has_object_permission method is not called when creating objects,
        # so we call it explicitly here. See: https://github.com/tomchristie/django-rest-framework/issues/1103
        self.check_object_permissions(self.request, obj)
        return super(CourseAuthorViewSet, self).pre_save(obj)

    def get_queryset(self):
        queryset = super(CourseAuthorViewSet, self).get_queryset()
        # is_course_author = self.request.QUERY_PARAMS.get('is_course_author', None)
        # if is_course_author == 'true':
        #     queryset = queryset.filter(is_course_author=True)
        # if is_course_author == 'false':
        #     queryset = queryset.filter(is_course_author=False)

        has_user = self.request.QUERY_PARAMS.get('has_user', None)
        if has_user:
            queryset = queryset.exclude(user=None)
        return queryset


class CoursePictureUploadViewSet(viewsets.ModelViewSet):
    model = CourseAuthor
    lookup_field = 'id'
    serializer_class = CourseAuthorPictureSerializer

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
    filter_fields = ('course__slug', 'course__id', 'user',)
    #     filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = CourseStudentSerializer

    def get_queryset(self):
        queryset = super(CourseStudentViewSet, self).get_queryset()
        if self.request.GET.get('user', False):
            return queryset
        return queryset.filter(user=self.request.user)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):

    model = get_user_model()
    serializer_class = ProfileSerializer

    def list(self, request, *args, **kwargs):

        username = self.request.QUERY_PARAMS.get('username', False)
        if username:
            serializer = self.serializer_class(self.model.objects.get(username=username))
            return Response(serializer.data)
        # SECURITY NOTE: this condition ensures the list of all users won't be exposed!
        elif self.request.user:
            serializer = self.serializer_class(self.request.user)
            return Response(serializer.data)
        else:
            return super(ProfileViewSet, self).list(self, request, *args,
                                                    **kwargs)


class CourseCertificationViewSet(viewsets.ModelViewSet):
    model = CourseCertification
    lookup_field = 'link_hash'
    filter_fields = ('course_student',)
    serializer_class = CourseCertificationSerializer

    def get_queryset(self):
        queryset = super(CourseCertificationViewSet, self).get_queryset()
        if not self.request.GET.get('user', False):
            queryset = queryset.filter(course_student__user=self.request.user)

        return queryset


class CourseCertificationDetailView(DetailView):
    model = CourseCertification
    template_name = 'certificate.html'
    slug_field = "link_hash"
    serializer_class = CourseCertificationSerializer

    def get_queryset(self, *args, **kwargs):
        return super(CourseCertificationDetailView, self).get_queryset(*args,
                                                                       **kwargs)

    def render_to_response(self, context, **response_kwargs):
        from django.core.urlresolvers import resolve

        certificate = context.get('object')
        if not certificate.course_student.can_emmit_receipt():
            raise Http404

        if certificate:
            context['cert_template'] = IfCertificateTemplate.objects.get(course=certificate.course_student.course)

        url_name = resolve(self.request.path_info).url_name

        if url_name == 'certificate-download':
            from selenium import webdriver
            from signal import SIGTERM
            from time import gmtime, strftime
            from timtec.settings import MEDIA_ROOT, CERTIFICATE_SIZE, PHANTOMJS_PATH
            from PIL import Image
            import os

            today = strftime("%d%b%Y", gmtime())

            width, height = CERTIFICATE_SIZE
            url = self.request.build_absolute_uri().split('download')[0] + 'print/'
            png_path = os.path.join(MEDIA_ROOT, certificate.link_hash + '.png')
            pdf_filename = certificate.link_hash + today + '.pdf'
            pdf_path = os.path.join(MEDIA_ROOT, pdf_filename)

            driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
            driver.set_window_size(width, height)
            driver.get(url)
            driver.save_screenshot(filename=png_path)

            driver.service.process.send_signal(SIGTERM)
            driver.quit()
            Image.open(png_path).convert("RGB").save(pdf_path, format='PDF', quality=100, dpi=(300, 300))

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s' % pdf_filename

            certi = open(pdf_path)
            response.write(certi.read())
            certi.close()

            return response
        else:
            return super(CourseCertificationDetailView, self)\
                .render_to_response(context, **response_kwargs)


class CertificationProcessViewSet(viewsets.ModelViewSet):
    model = CertificationProcess
    filter_fields = ('student',)
    serializer_class = CertificationProcessSerializer

    permission_classes = []

    def get_queryset(self):
        queryset = super(CertificationProcessViewSet, self).get_queryset()

        klass = self.request.QUERY_PARAMS.get('klass')
        if klass:
            queryset = queryset.filter(klass=klass)

        return queryset


class EmitReceiptView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        course_id = kwargs.get('course_id')
        if course_id:
            course_student = CourseStudent.objects.get(course__id=course_id, user=self.request.user)
        else:
            return reverse_lazy('courses')

        if course_student and course_student.can_emmit_receipt():
            recipt = CourseCertification()
            recipt.course_student = course_student
            recipt.course_workload = course_student.course.workload
            recipt.is_valid = True
            recipt.type = 'recipt'

            import hashlib
            import time
            hash = hashlib.sha1()
            hash.update(str(time.time()))
            recipt.link_hash = hash.hexdigest()[:10]
            recipt.save()
            return reverse_lazy('certificate', args=[recipt.link_hash])
        else:
            return reverse_lazy('course_intro', args=[course_student.course.slug])


class RequestCertificateView(View):
    # CertificationProcess
    pass


class CertificateTemplateViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = IfCertificateTemplate
    lookup_field = 'course'

    serializer_class = IfCertificateTemplateSerializer

    def update(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class CertificateTemplateImageViewSet(viewsets.ModelViewSet):
    model = CertificateTemplate
    lookup_field = 'course'
    serializer_class = CertificateTemplateImageSerializer
    permission_classes = (IsProfessorCoordinatorOrAdminPermissionOrReadOnly, )

    def post(self, request, **kwargs):
        certificate_template = self.get_object()
        serializer = CertificateTemplateImageSerializer(
            certificate_template, request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)


class ProfessorMessageViewSet(viewsets.ModelViewSet):
    model = ProfessorMessage
    lookup_field = 'id'
    filter_fields = ('course',)
    filter_backends = (filters.DjangoFilterBackend,)

    def get_serializer_class(self):
        if 'id' in self.kwargs.keys():
            return ProfessorMessageUserDetailsSerializer
        return ProfessorMessageSerializer

    def pre_save(self, obj):
        obj.professor = self.request.user
        return super(ProfessorMessageViewSet, self).pre_save(obj)

    def post_save(self, obj, created):
        if created:
            obj.send()

    # TODO tests for this
    def get_queryset(self, *args, **kwargs):
        queryset = super(ProfessorMessageViewSet, self).get_queryset(*args, **kwargs)
        if not self.request.user.is_superuser:
            queryset = queryset.filter(users=self.request.user)
        return queryset


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
            queryset = queryset.filter(status='published').prefetch_related('professors')
        role = self.request.QUERY_PARAMS.get('role', None)
        if role and not self.request.user.is_superuser:
            queryset = queryset.filter(
                course_professors__role=role,
                course_professors__user=self.request.user
            ).prefetch_related('professors')

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
    queryset = Course.objects.exclude(status=Course.STATES[0][0]).filter(start_date__gte=datetime.date.today())
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
    fields = ('name', 'assistant', 'user_can_certificate',)

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


class ClassEvaluationsView(LoginRequiredMixin, CanEditClassMixin, UpdateView):
    model = Class
    template_name = 'evaluations.html'

    fields = []


class EvaluationViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = Evaluation
    ordering = ('date',)

    filter_fields = ('klass',)
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_class = EvaluationSerializer

    # def get_queryset(self):
    #    queryset = super(EvaluationViewSet, self.get_queryset())

    #    klass_id = self.request.QUERY_PARAMS.get('klass_id')
    #    if klass_id:


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
    lookup_field = 'unit'
    filter_fields = ('unit', 'unit__lesson',)
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = StudentProgressSerializer

    def update(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        if self.object:
            self.object.save()
            # TODO: verificar se a resposta deveria ser esta mesmo.
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
            unit_type = ContentType.objects.get_for_model(unit)
            note = get_object_or_404(Note, user=user, content_type__pk=unit_type.id, object_id=unit.id)
            unit.user_note = note
            courses[course.slug].lessons_dict[lesson.slug].units_notes.append(unit)

        results = []
        for course in courses.values():
            course.lessons_notes = course.lessons_dict.values()
            course.course_notes_number = Unit.objects.filter(lesson__course=course, notes__user=user).exclude(notes__isnull=True).count()
            del course.lessons_dict
            results.append(CourseNoteSerializer(course).data)
        return Response(results)


class ClassViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

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


class FlatpageView(View):

    def get(self, request, url):
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'

        from django.contrib.flatpages.views import flatpage, render_flatpage

        if not request.user.is_superuser or FlatPage.objects.filter(url='url', sites=settings.SITE_ID).exists():
            return flatpage(request, url)
        else:
            f = FlatPage(url=url)
            return render_flatpage(request, f)


class FlatpageViewSet(viewsets.ModelViewSet):

    model = FlatPage
    serializer_class = FlatpageSerializer
    filter_fields = ('url',)
    permission_classes = (IsAdminOrReadOnly,)

    def post_save(self, obj, created=False):
        if created:
            from django.contrib.sites.models import Site
            obj.sites.add(Site.objects.get(id=settings.SITE_ID))
            obj.save()

    def get_queryset(self):
        queryset = super(FlatpageViewSet, self).get_queryset()
        url_prefix = self.request.QUERY_PARAMS.get('url_prefix')
        if url_prefix:
            queryset = queryset.filter(url__startswith=url_prefix)
        return queryset
