from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)$/',
        TemplateView.as_view(template_name="new_course.html"),
        name='course_admin'),

    url(r'^courses/$', TemplateView.as_view(template_name="courses.html")),
    url(r'^courses/new/$', TemplateView.as_view(template_name="new_course.html")),
    url(r'^courses/(?P<pk>[1-9][0-9]*)/$', TemplateView.as_view(template_name="new_course.html")),
    url(r'^courses/lessons/new/$', TemplateView.as_view(template_name="new_lesson.html")),
    url(r'^users/$', TemplateView.as_view(template_name="users.html")),
)
