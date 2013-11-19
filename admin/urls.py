from django.conf.urls import patterns, url

from views import AdminCourseView

urlpatterns = patterns(
    '',
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)$', AdminCourseView.as_view(), name='course_admin'),
)
