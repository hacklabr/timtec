# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from core.views import CourseIntroView, HomeView
from accounts.views import RegistrationView, CustomLoginView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_view'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)/?$', CourseIntroView.as_view(), name='course_intro'),
    url(r'^lesson/', 'core.views.lesson', name='lesson'),

    # Authentication
    url(r'^login/', CustomLoginView.as_view(), name='timtec_login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='timtec_logout'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # The django-registration
    url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # The django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),
)
