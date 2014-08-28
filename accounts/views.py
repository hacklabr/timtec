from django.contrib.auth import get_user_model
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q

from accounts.forms import ProfileEditForm
from accounts.serializers import TimtecUserSerializer
from braces.views import LoginRequiredMixin

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics


class CustomLoginView(TemplateView):
    """
    Change template context name of form to login_form

    """
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data()
        default_next = reverse_lazy('home_view')
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
        # check if the email was verified first
        from allauth.account.models import EmailAddress
        try:
            ea = EmailAddress.objects.get(Q(user__username=self.request.POST['username']) | Q(user__email=self.request.POST['username']))
        except EmailAddress.DoesNotExist:
            # if it doens't exist in the EmailAddress database, it's an old
            # registration, let's authorize
            pass
        else:
            if not ea.verified:
                return redirect('account_email_verification_sent')
        ret = login(self.request, template_name=CustomLoginView.template_name)
        if type(ret) is TemplateResponse:
            ret.context_data['login_form'] = ret.context_data.pop('form')
        return ret


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileEditForm
    template_name = 'profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile')

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


class TimtecUserViewSet(viewsets.ModelViewSet):
    model = get_user_model()
    lookup_field = 'id'
    filter_fields = ('groups__name',)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    serializer_class = TimtecUserSerializer
    ordering = ('first_name', 'username',)


class UserSearchView(LoginRequiredMixin, generics.ListAPIView):
    model = get_user_model()
    serializer_class = TimtecUserSerializer

    def get_queryset(self):
        """
        This view should return a list of
            if q, all tags that contain q
            else, all tags
        """
        queryset = self.model.objects.all()
        query = self.request.QUERY_PARAMS.get('name', None)
        if query is not None:
            queryset = queryset.filter(Q(first_name__icontains=query) |
                                       Q(last_name__icontains=query) |
                                       Q(username__icontains=query) |
                                       Q(email__icontains=query))
        return queryset
