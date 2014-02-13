from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required as lr
from forum.views import AdminCourseForumView

urlpatterns = patterns(
    '',
    # list all courses
    url(r'^$', lr(RedirectView.as_view(url="courses/")), name="administration.home"),
    url(r'^courses/$', lr(TemplateView.as_view(template_name="courses.html"))),

    # create and edit course
    url(r'^courses/new/$', lr(TemplateView.as_view(template_name="new_course.html"))),
    url(r'^courses/(?P<pk>[1-9][0-9]*)/$', lr(TemplateView.as_view(template_name="new_course.html"))),

    # create and edit lesson
    url(r'^courses/(?P<course_id>[1-9][0-9]*)/lessons/new/$', lr(TemplateView.as_view(template_name="new_lesson.html"))),
    url(r'^courses/(?P<course_id>[1-9][0-9]*)/lessons/(?P<pk>[1-9][0-9]*)/$', lr(TemplateView.as_view(template_name="new_lesson.html"))),

    # messages
    url(r'^course/(?P<course_id>[1-9][0-9]*)/messages/$', lr(TemplateView.as_view(template_name="messages.html"))),
    url(r'^course/(?P<course_id>[1-9][0-9]*)/message/$', lr(TemplateView.as_view(template_name="message.html"))),

    url(r'^course/(?P<course_id>[1-9][0-9]*)/forum/', AdminCourseForumView.as_view()),

    url(r'^users/$', lr(TemplateView.as_view(template_name="users.html"))),

    url(r'^course/(?P<course_id>[1-9][0-9]*)/stats/$', lr(TemplateView.as_view(template_name="stats.html"))),
)
