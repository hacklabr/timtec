# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from core.views import CourseIntroView
from accounts.views import RegistrationView

urlpatterns = patterns(
    '',
    url(r'^$', CourseIntroView.as_view(), name='course-intro'),
    url(r'^lesson/', 'core.views.lesson', name='lesson'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # django-registration
    url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),
)
