# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from braces import views
from core.models import Course
from django.contrib.auth import get_user_model
import django_filters


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


class UserListView(AdminMixin, ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'user_list'
    paginate_by = 100

    def get_queryset(self):
        qs = super(UserListView, self).get_queryset().prefetch_related('groups')
        f = UserFilter(self.request.GET, queryset=qs)
        return f.qs  # .filter(is_superuser=self.kwargs['admin'])

class CourseAdminView(AdminMixin, DetailView):
    model = Course
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'
