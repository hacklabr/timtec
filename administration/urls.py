from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required as lr
from forum.views import AdminCourseForumView
from course_material.views import CourseMaterialAdminView
from .views import (AdminView, CourseAdminView, CourseCreateView,
                    ExportCourseView, ImportCourseView, UserAdminView,)

urlpatterns = patterns(
    '',
    # home admin
    url(r'^home/$', lr(AdminView.as_view(template_name="home.html")), name="administration.home"),

    # list all courses
    url(r'^$', lr(RedirectView.as_view(url="courses/", permanent=False))),
    url(r'^courses/$', AdminView.as_view(template_name="courses.html"), name='administration.courses'),

    # users
    url(r'^users/$', UserAdminView.as_view(template_name="users.html"), name='administration.users'),
    # url(r'^users/(?P<pk>[0-9]+)/$', UserUpdateView.as_view(), name='administration.user-update'),
    # url(r'^users/(?P<pk>[0-9]+)/delete/$', UserDeleteView.as_view(), name='administration.user-delete'),

    # create, edit and export courses
    url(r'^courses/new/$', CourseCreateView.as_view(), name="administration.new_course"),
    url(r'^courses/(?P<course_id>[1-9][0-9]*)/$', CourseAdminView.as_view(template_name="course.html"), name="administration.edit_course"),
    url(r'^course/(?P<course_id>[1-9][0-9]*)/export/$', ExportCourseView.as_view(), name="administration.export_course"),
    url(r'^course/import/$', ImportCourseView.as_view(), name="administration.import_course"),

    # create and edit lesson
    url(r'^courses/(?P<course_id>[1-9][0-9]*)/lessons/new/$', CourseAdminView.as_view(template_name="lesson.html")),
    url(r'^courses/(?P<course_id>[1-9][0-9]*)/lessons/(?P<pk>[1-9][0-9]*)/$', CourseAdminView.as_view(template_name="lesson.html")),

    # messages
    url(r'^course/(?P<course_id>[1-9][0-9]*)/messages/$', CourseAdminView.as_view(template_name="messages.html"), name="administration.messages"),
    url(r'^course/(?P<course_id>[1-9][0-9]*)/message/(?P<message_id>[1-9][0-9]*)$', CourseAdminView.as_view(template_name="message.html")),

    url(r'^course/(?P<course_id>[1-9][0-9]*)/forum/', AdminCourseForumView.as_view(template_name="forum.html"), name="administration.forum"),

    url(r'^course/(?P<pk>[1-9][0-9]*)/material/$',
        CourseMaterialAdminView.as_view(template_name="course-material-admin.html"),
        name="administration.course_material"
        ),

    url(r'^course/(?P<course_id>[1-9][0-9]*)/permissions/$', CourseAdminView.as_view(template_name="permissions.html"), name="course.permissions"),

    url(r'^course/(?P<course_id>[1-9][0-9]*)/certificatesettings/$', CourseAdminView.as_view(template_name="certificate-settings.html"), name="course.certificate-settings"),

    url(r'^course/(?P<course_id>[1-9][0-9]*)/reports/$', CourseAdminView.as_view(template_name="stats.html"), name="administration.reports"),

)
