# -*- coding: utf-8 -*-
from django import forms
from course_material.models import File


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['file', 'course_material']
