# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm


class BaseUserChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = True
        self.fields['password2'].required = True

    email = forms.RegexField(label=_("email"), max_length=75, regex=r"^[\w.@+-]+$")

    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=False)

    accept_terms = forms.BooleanField(label=_('Accept '), initial=False, required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_accept_terms(self):
        data = self.cleaned_data.get('accept_terms')
        if settings.TERMS_ACCEPTANCE_REQUIRED and not data:
                raise forms.ValidationError(_('You must agree to the Terms of Use to use %(site_name)s.'),
                                            params={'site_name': settings.SITE_NAME},)
        return data


class SignupStudentCompletion(BaseUserChangeForm):

    def __init__(self, *args, **kwargs):
        super(SignupStudentCompletion, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['city'].required = True
        self.fields['ifid'].required = True
        self.fields['course'].required = True
        self.fields['klass'].required = True
        self.fields['campus'].required = True

    class Meta:
        model = get_user_model()
        fields = ('ifid', 'first_name', 'last_name', 'email', 'campus', 'city', 'course', 'klass')

    def save(self, **kwargs):
        user = super(SignupStudentCompletion, self).save(commit=False)
        user.ifid = self.cleaned_data['ifid']
        user.course = self.cleaned_data['course']
        user.klass = self.cleaned_data['klass']
        user.campus = self.cleaned_data['campus']
        user.city = self.cleaned_data['city']
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        user.accepted_terms = self.cleaned_data['accept_terms']
        user.save()


class SignupProfessorCompletion(BaseUserChangeForm):

    def __init__(self, *args, **kwargs):
        super(SignupProfessorCompletion, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['city'].required = True
        self.fields['siape'].required = True
        self.fields['cpf'].required = True
        self.fields['campus'].required = True

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'campus', 'city', 'siape', 'cpf')

    def save(self, **kwargs):
        user = super(SignupProfessorCompletion, self).save(commit=False)
        user.ifid = self.cleaned_data['siape']
        user.course = self.cleaned_data['cpf']
        user.campus = self.cleaned_data['campus']
        user.city = self.cleaned_data['city']
        if self.cleaned_data['password2']:
            user.set_password(self.cleaned_data['password2'])
        user.accepted_terms = self.cleaned_data['accept_terms']
        user.save()


class IfSignupForm(BaseUserChangeForm):

    def __init__(self, *args, **kwargs):
        super(IfSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['city'].required = True
        # self.fields['campus'] = forms.ModelChoiceField(queryset=Campus.objects.all())

    if_student = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'campus', 'city', 'course', 'klass')

    def clean_username(self):
        data = self.cleaned_data['username']
        if not data:
            if 'if_student' in self.data:
                raise forms.ValidationError('O campo código de matrícula é obrigatório para alunos do IFSUL.')
            else:
                super(IfSignupForm, self).clean_username(self)
        return data

    def clean_course(self):
        data = self.cleaned_data['course']
        if 'if_student' in self.data and not data:
            raise forms.ValidationError('O campo curso é obrigatório para alunos do IFSUL.')
        return data

    def clean_klass(self):
        data = self.cleaned_data['klass']
        if 'if_student' in self.data and not data:
            raise forms.ValidationError('O campo turma é obrigatório para alunos do IFSUL.')
        return data

    def clean_campus(self):
        data = self.cleaned_data['campus']
        if 'if_student' in self.data and not data:
            raise forms.ValidationError('O campo campus é obrigatório para alunos do IFSUL.')
        return data

    def signup(self, request, user):
        if 'if_student' in self.data:
            user.ifid = self.cleaned_data['username']
            user.course = self.cleaned_data['course']
            user.klass = self.cleaned_data['klass']
            user.campus = self.cleaned_data['campus']
            user.city = self.cleaned_data['city']
            user.is_if_staff = True
            user.accepted_terms = self.cleaned_data['accept_terms']
            user.save()


class IfLoginForm(LoginForm):
    def login(self, request, redirect_url=None):
        response = super(IfLoginForm, self).login(request, redirect_url)
        if self.user.is_authenticated():
            if self.user.is_if_staff:
                if request.user.groups.filter(name='professors').exists():
                    if not (self.user.campus and self.user.cpf and self.user.siape):
                        url = reverse_lazy('signup_completion')
                        url += '?next=' + response.url
                        return redirect(url)
                else:
                    if not (self.user.campus and self.user.klass and self.user.course and self.user.ifid):
                        url = reverse_lazy('signup_completion')
                        url += '?next=' + response.url
                        return redirect(url)
        return response
