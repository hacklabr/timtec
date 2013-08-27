# -*- coding: utf-8 -*-
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()
from django import forms
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    required_css_class = 'required'

    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"))

    def clean_email(self):
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class ProfileEditForm(forms.ModelForm):
    email = forms.RegexField(label=_("email"), max_length=75, regex=r"^[\w.@+-]+$")

    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password"), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Password (again)"), required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'picture', 'nickname',
                  'occupation', 'city', 'site', 'biography',)

    def clean_email(self):
        return self.instance.email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        if self.cleaned_data['password1']:
            self.instance.set_password(self.cleaned_data['password1'])
        return super(ProfileEditForm, self).save(commit=commit)
