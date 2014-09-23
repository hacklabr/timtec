# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Class, CourseStudent
import logging

logger = logging.getLogger(__name__)


class AcceptTermsForm(forms.Form):
    accept_terms = forms.BooleanField(label=_('Accept '), initial=False, required=True)


class ContactForm(forms.Form):
    occupation = forms.CharField(label=_('Occupation'), max_length=128)
    subject = forms.CharField(label=_('Subject'), max_length=128)
    name = forms.CharField(label=_('Name'), max_length=128)
    email = forms.EmailField(label=_('Email'))
    message = forms.CharField(label=_('Message'), max_length=255)

    def send_email(self):
        subject = self.cleaned_data.get('subject')
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        message = self.cleaned_data.get('message')
        message_from = 'From %s <%s>' % (name, email,)
        message = message_from + '\n\n\n' + message

        recipient_list = settings.CONTACT_RECIPIENT_LIST
        sender = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, sender, recipient_list, fail_silently=False)


class SignupForm(forms.Form):
    accept_terms = forms.BooleanField(label=_('Accept '), initial=True, required=True)

    def save(self, user):
        user.accepted_terms = True
        user.save()


class RemoveStudentForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = []

    user_id = forms.IntegerField()

    def save(self, commit=True):
        uid = self.cleaned_data['user_id']
        self.instance.remove_students(get_user_model().objects.get(id=uid))
        return super(RemoveStudentForm, self).save(commit=commit)


class AddStudentsForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = []

    students_text = forms.CharField()

    def clean_students_text(self):
        data = self.cleaned_data['students_text'].strip().split()
        data = [u.strip() for u in data]
        return data

    def save(self, commit=True):
        User = get_user_model()
        students = self.cleaned_data['students_text']
        for student_name in students:
            try:
                student = User.objects.get(username=student_name)
            except User.DoesNotExist:
                logger.info(u'student with username: %s does not exist' % student_name)

            self.instance.add_students(student)
        return super(AddStudentsForm, self).save(commit=commit)
