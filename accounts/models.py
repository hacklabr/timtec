# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group
from django.utils import timezone

from core.utils import hash_name
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError
import re
import json


class AbstractTimtecUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_REGEXP = re.compile('^[\w.+-]+$')
    username = models.CharField(
        _('Username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    './+/-/_ characters'),
        validators=[
            validators.RegexValidator(USERNAME_REGEXP, _('Enter a valid username.'), 'invalid')
        ])

    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    picture = models.ImageField(_("Picture"), upload_to=hash_name('user-pictures', 'username'), blank=True)
    occupation = models.CharField(_('Occupation'), max_length=127, blank=True)
    city = models.CharField(_('City'), max_length=30, blank=True)
    site = models.URLField(_('Site'), blank=True)
    biography = models.TextField(_('Biography'), blank=True)
    accepted_terms = models.BooleanField(_('Accepted terms and condition'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def __unicode__(self):
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.email

    def get_picture_url(self):
        if not self.picture:
            location = "/%s/%s" % (settings.STATIC_URL, 'img/avatar-default.png')
        else:
            location = "/%s/%s" % (settings.MEDIA_URL, self.picture)
        return re.sub('/+', '/', location)

    def get_picture_thumb_url(self,
                              options={'size': (150, 150), 'crop': 'scale'}):
        try:
            return get_thumbnailer(self.picture).get_thumbnail(options).url
        except InvalidImageFormatError as e:
            return str(settings.STATIC_URL + 'img/avatar-default.png')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_group_names(self):
        group_names = self.groups.all().values_list("name", flat=True)
        return json.dumps({
            'names': list(map(lambda g: unicode(g), group_names))
        })

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def get_user_type(self):
        if self.is_superuser:
            return "superuser"
        elif self.groups.filter(name='professors').count():
            return "professors"
        elif self.groups.filter(name='students').count():
            return "students"
        return "unidentified"

    def is_pilot(self):
        return self.groups.filter(name='pilot_course').count() > 0

    @property
    def is_profile_filled(self):
        from timtec.settings import ACCOUNT_REQUIRED_FIELDS as fields

        for field in fields:
            try:
                f = getattr(self, field)
                if not f:
                    return False
            except AttributeError:
                raise AttributeError(_('Invalid attribute: %s' % field))
        return True

    def get_certificates(self):
        from core.models import CourseCertification
        return CourseCertification.objects.filter(course_student__user=self)

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super(AbstractTimtecUser, self).save(*args, **kwargs)

        if is_new and settings.REGISTRATION_DEFAULT_GROUP_NAME:
            try:
                self.groups.add(Group.objects.get(name=settings.REGISTRATION_DEFAULT_GROUP_NAME))
                self.save()
            except Group.DoesNotExist:
                pass


class TimtecUser(AbstractTimtecUser):
    """
    Timtec customized user.

    Username, password and email are required. Other fields are optional.
    """

    email = models.EmailField(_('Email address'), blank=False, unique=True)
    cpf = models.CharField(max_length=11, blank=True, null=True, unique=True)
    institution = models.CharField(max_length=255, blank=True, null=True)

    class Meta(AbstractTimtecUser.Meta):
        swappable = 'AUTH_USER_MODEL'
