# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.edit import ModelFormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.conf import settings
from django.utils.six import BytesIO
from braces import views
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from core.models import Course
from .forms import UserUpdateForm
from .serializer import CourseImportExportSerializer

import tarfile
import StringIO
import os


User = get_user_model()


class AdminMixin(TemplateResponseMixin, ContextMixin,):
    def get_context_data(self, **kwargs):
        context = super(AdminMixin, self).get_context_data(**kwargs)
        context['in_admin'] = True
        return context

    def get_template_names(self):
        """
        Returns two template options, either the administration specific
        or the common template
        """
        return ['administration/' + self.template_name, self.template_name]


class AdminView(views.GroupRequiredMixin, AdminMixin, TemplateView):
    group_required = u'professors'
    raise_exception = True


class UserListView(views.SuperuserRequiredMixin, AdminMixin, ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'user_list'
    paginate_by = 50
    raise_exception = True

    def get_queryset(self):
        qs = super(UserListView, self) \
            .get_queryset() \
            .prefetch_related('groups') \
            .order_by('username')
        print self.request.GET
        if self.request.GET.get('admin', '').lower() == 'on':
            qs = qs.filter(is_superuser=True)
        if self.request.GET.get('professors', '').lower() == 'on':
            qs = qs.filter(groups__name='professors')
        if self.request.GET.get('keyword', '') != '':
            qs = qs.filter(username__icontains=self.request.GET.get('keyword'))
        return qs


class UserUpdateView(views.SuperuserRequiredMixin, AdminMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'base.html'
    raise_exception = True

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form))

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(str(context['form'].errors))


class UserDeleteView(views.SuperuserRequiredMixin, DeleteView):
    model = User
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse('ok')


class CourseAdminView(views.GroupRequiredMixin, AdminMixin, DetailView):
    model = Course
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'
    group_required = u'professors'
    raise_exception = True


class CourseCreateView(views.SuperuserRequiredMixin, View, ModelFormMixin):
    model = Course
    fields = ('name',)
    raise_exception = True

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        base_slug = slugify(form.instance.name)
        slug = base_slug
        i = 1
        while Course.objects.filter(slug=slug).exists():
            slug = base_slug + str(i)
            i += 1
        form.instance.slug = slug
        return super(CourseCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('administration.courses'))

    def get_success_url(self):
        return reverse_lazy('administration.edit_course', kwargs={'course_id': self.object.id})


class ExportCourseView(views.SuperuserRequiredMixin, View):

    @staticmethod
    def add_files_to_export(tar_file, short_file_path):
        full_file_path = settings.MEDIA_ROOT + '/' + short_file_path
        if os.path.isfile(full_file_path):
                tar_file.add(full_file_path,
                             arcname=short_file_path)

    def get(self, request, *args, **kwargs):

        course_id = kwargs.get('course_id')
        course = Course.objects.get(id=course_id)

        course_serializer = CourseImportExportSerializer(course)

        json_file = StringIO.StringIO(JSONRenderer().render(course_serializer.data))

        tar_info = tarfile.TarInfo('course.json')
        tar_info.size = json_file.len

        filename = course.slug + '.tar.gz'

        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        course_tar_file = tarfile.open(fileobj=response, mode='w:gz')
        course_tar_file.addfile(tar_info, json_file)

        course_professors = course_serializer.data.get('course_professors')
        for course_professor in course_professors:
            picture_path = course_professor.get('picture')
            if picture_path:
                picture_path = picture_path.split('/', 2)[-1]
                self.add_files_to_export(course_tar_file, picture_path)

        course_thumbnail_path = course_serializer.data.get('thumbnail')
        if course_thumbnail_path:
            self.add_files_to_export(course_tar_file, course_thumbnail_path)

        course_home_thumbnail_path = course_serializer.data.get('home_thumbnail')
        if course_home_thumbnail_path:
            self.add_files_to_export(course_tar_file, course_home_thumbnail_path)

        course_material = course_serializer.data.get('course_material')
        if course_material:
            course_material = course_material[0]
        for course_material_file in course_material['files']:
            course_material_file_path = course_material_file['file']
            self.add_files_to_export(course_tar_file, course_material_file_path)

        return response


class ImportCourseView(views.SuperuserRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        import_file = tarfile.open(fileobj=request.FILES.get('course-import-file'))
        file_names = import_file.getnames()
        json_file_name = [s for s in file_names if '.json' in s][0]

        json_file = import_file.extractfile(json_file_name)
        # course_data = json_file.read()

        stream = BytesIO(json_file.read())
        course_data = JSONParser().parse(stream)
        course_slug = course_data.get('slug')
        try:
            course = Course.objects.get(slug=course_slug)
            if course.has_started:
                pass
                # abort importing.
        except Course.DoesNotExist:
            pass

        # home_thumbnail = slug = course_data.pop('home_thumbnail')
        # thumbnail = slug = course_data.pop('thumbnail')

        course_serializer = CourseImportExportSerializer(data=course_data)

        if course_serializer.is_valid():
            course_serializer.save()
            return reverse_lazy('administration.edit_course', kwargs={'course_id': course_serializer.object.id})
