from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required as lr

urlpatterns = patterns(
    '',
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)$/',
        lr(TemplateView.as_view(template_name="new_course.html")),
        name='course_admin'),

    url(r'^courses/$', lr(TemplateView.as_view(template_name="courses.html"))),
    url(r'^courses/new/$', lr(TemplateView.as_view(template_name="new_course.html"))),
    url(r'^courses/(?P<pk>[1-9][0-9]*)/$', lr(TemplateView.as_view(template_name="new_course.html"))),
    url(r'^courses/lessons/new/$', lr(TemplateView.as_view(template_name="new_lesson.html"))),
    url(r'^users/$', lr(TemplateView.as_view(template_name="users.html"))),
)
