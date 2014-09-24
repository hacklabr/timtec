# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django import forms
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm


class IfSignupForm(forms.ModelForm):
    email = forms.RegexField(label=_("email"), max_length=75, regex=r"^[\w.@+-]+$")

    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=False)
    if_student = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('ifid', 'first_name', 'last_name', 'email', 'campus', 'city', 'course', 'klass')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_ifid(self):
        data = self.cleaned_data['ifid']
        if 'if_student' in self.data and not data:
            raise forms.ValidationError('O campo código de matrícula é obrigatório para alunos do IFSUL.')
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

    def save(self, user):
        if 'if_student' in self.data:
            user.ifid = self.cleaned_data['ifid']
            user.course = self.cleaned_data['course']
            user.klass = self.cleaned_data['klass']
            user.campus = self.cleaned_data['campus']
            user.campus.is_if_student = True
            user.save()


class IfLoginForm(LoginForm):
    def login(self, request, redirect_url=None):
        response = super(IfLoginForm, self).login(request, redirect_url)
        # if self.user.is_authenticated():
        #     if not self.user.email or
        #     return HttpResponseRedirect(r)

        return response


class SignupStudentCompletion(forms.ModelForm):
    pass


class SignupProfessorCompletion(forms.ModelForm):
    pass