# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from core.views import CourseIntroView, HomeView
from accounts.views import CustomLoginView, ProfileEditView
from lesson.views import LessonDetailView

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_view'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)$', CourseIntroView.as_view(), name='course_intro'),
    url(r'^lesson/(?P<slug>[-a-zA-Z0-9_]+)$', LessonDetailView.as_view(), name='lesson'),

    # Authentication
    url(r'^login/', CustomLoginView.as_view(), name='timtec_login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='timtec_logout'),

    url(r'^profile/edit/?$', ProfileEditView.as_view(), name="profile_edit"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # The django-registration
    url(r'^accounts/', include('registration.backends.default.urls')),

    # The django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)