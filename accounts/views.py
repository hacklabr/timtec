from django.contrib.auth import get_user_model
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

from forms import ProfileEditForm
from utils import LoginRequiredMixin


class RegistrationUniqueEmailView(RegistrationView):
    form_class = RegistrationFormUniqueEmail


class CustomLoginView(TemplateView):
    """
    Change template context name of form to login_form

    """
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data()
        default_next = reverse('home_view')
        next_step = self.request.REQUEST.get('next', default_next)

        if not is_safe_url(next_step):
            next_step = default_next

        context['next'] = next_step
        return context

    def get(self, *argz, **kwargs):
        context = self.get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            return redirect(context.get('next'))

        return self.render_to_response(context)

    def post(self, *argz, **kwargs):
        ret = login(self.request, template_name=CustomLoginView.template_name)
        if type(ret) is TemplateResponse:
            ret.context_data['login_form'] = ret.context_data.pop('form')
        return ret


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'profile-edit.html'

    def get_success_url(self):
        return reverse('profile_edit')

    def get_object(self):
        return self.request.user


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        if hasattr(self, 'kwargs') and 'username' in self.kwargs:
            try:
                return get_object_or_404(self.model, username=self.kwargs['username'])
            except:
                return self.request.user
        else:
            return self.request.user
