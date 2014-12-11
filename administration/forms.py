# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = []

    action = forms.ChoiceField(choices='professors is_superuser'.split())
    value = forms.BooleanField(required=False)

    def save(self, commit=True):
        user = self.instance
        action = self.cleaned_data['action']
        value = self.cleaned_data['value']
        if action == 'is_superuser':
            user.is_superuser = value
            user.save()
        elif action == 'professors':
            g = Group.objects.get(name='professors')
            if value:
                user.groups.add(g)
            else:
                user.groups.remove(g)

        return super(UserUpdateForm, self).save(commit=commit)
