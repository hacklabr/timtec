# -*- coding: utf-8 -*-
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from braces.views import LoginRequiredMixin
from .forms import SignupStudentCompletion, SignupProfessorCompletion


class SignupCompletionView(LoginRequiredMixin, UpdateView):
    """
    This view is used to complete missing imported professors and students information if they
    are not present after login.
    """
    model = get_user_model()
    template_name = 'ifs/signup-completion.html'

    def get_success_url(self):
        url = self.request.REQUEST.get('next', None)
        if url:
            return url
        else:
            return '/'

    def get_form_class(self):
        # decide to user professor or student signup completion form
        if self.request.user.groups.filter(name='professors').exists():
            return SignupProfessorCompletion
        else:
            return SignupStudentCompletion

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(SignupCompletionView, self).get_context_data(**kwargs)
        context['is_professor'] = self.request.user.groups.filter(name='professors').exists()
        return context
