# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from braces import views


class AdminView(views.LoginRequiredMixin, views.GroupRequiredMixin, TemplateView):
    template_name = '_base.html'
    group_required = u'professors'
    raise_exception = True
