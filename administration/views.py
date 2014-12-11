# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from braces import views
import django_filters
from core.models import Course
from .forms import UserUpdateForm


User = get_user_model()


class AdminMixin(views.LoginRequiredMixin, views.GroupRequiredMixin, TemplateResponseMixin, ContextMixin,):
    group_required = u'professors'
    raise_exception = True

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


class AdminView(AdminMixin, TemplateView):
    pass


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['email', 'is_superuser', ]
        order_by = ['email', ]


class UserListView(AdminMixin, ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'user_list'
    paginate_by = 100

    def get_queryset(self):
        qs = super(UserListView, self).get_queryset().prefetch_related('groups')
        f = UserFilter(self.request.GET, queryset=qs)
        return f.qs  # .filter(is_superuser=self.kwargs['admin'])


class UserUpdateView(AdminMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'base.html'

    def form_valid(self, form):
        form.save()
        return self.render_to_response(self.get_context_data(form=form))

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(str(context['form'].errors))


class UserDeleteView(AdminMixin, DeleteView):
    model = User


class CourseAdminView(AdminMixin, DetailView):
    model = Course
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'
