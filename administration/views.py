# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from braces import views


class AdminView(views.LoginRequiredMixin, views.GroupRequiredMixin, TemplateView):
    group_required = u'professors'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(AdminView, self).get_context_data(**kwargs)
        context['in_admin'] = True
        return context

    # def get_template_names(self):
    #     """
    #     Returns two template options, either the administration specific
    #     or the common template
    #     """
    #     return ['administration/' + self.template_name, self.template_name]
