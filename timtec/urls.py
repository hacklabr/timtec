# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.course_intro', name='course-intro'),
    url(r'^lesson/', 'core.views.lesson', name='lesson'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # django-registration
    url(r'^accounts/', include('registration.backends.default.urls')),

    # django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),
)
