# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.views.generic import TemplateView
from accounts.views import (ProfileEditView, ProfileView, UserSearchView,
                            TimtecUserViewSet, StudentSearchView, AcceptTermsView)
from forum.views import AnswerViewSet as ForumAnswerViewSet, ForumModeratorView

from core.views import (CourseView, GenericCourseView, CourseViewSet,
                        CourseProfessorViewSet, EnrollCourseView, HomeView,
                        UserCoursesView, ContactView, LessonDetailView,
                        LessonViewSet, StudentProgressViewSet,
                        UserNotesViewSet, CoursesView, CourseThumbViewSet,
                        ProfessorMessageViewSet, CourseStudentViewSet,
                        CarouselCourseView, ClassListView,
                        ClassCreateView, ClassUpdateView, ClassDeleteView,
                        ClassRemoveUserView, ClassAddUsersView, ClassViewSet,
                        FlatpageViewSet, CoursePictureUploadViewSet,
                        ResumeCourseView, )

from activities.views import AnswerViewSet
from forum.views import CourseForumView, QuestionView, QuestionCreateView, QuestionViewSet, QuestionVoteViewSet, AnswerVoteViewSet
from course_material.views import CourseMaterialView, FileUploadView, CourseMaterialViewSet
from notes.views import NotesViewSet, CourseNotesView, UserNotesView
from reports.views import UserCourseStats, CourseStatsByLessonViewSet, UserCourseLessonsStats
from rest_framework import routers
from django_markdown import flatpages

# Uncomment the next two lines to enable the admin:
from django.contrib import admin as django_admin
django_admin.autodiscover()

flatpages.register()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', TimtecUserViewSet)
router.register(r'course', CourseViewSet)
router.register(r'course_carousel', CarouselCourseView)
router.register(r'course_professor', CourseProfessorViewSet)
router.register(r'course_professor_picture', CoursePictureUploadViewSet)
router.register(r'course_student', CourseStudentViewSet)
router.register(r'professor_message', ProfessorMessageViewSet)
router.register(r'coursethumbs', CourseThumbViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'student_progress', StudentProgressViewSet)
router.register(r'forum_question', QuestionViewSet)
router.register(r'forum_answer', ForumAnswerViewSet)
router.register(r'question_vote', QuestionVoteViewSet)
router.register(r'answer_vote', AnswerVoteViewSet)
router.register(r'course_material', CourseMaterialViewSet)
router.register(r'note', NotesViewSet)
router.register(r'user_notes', UserNotesViewSet)
router.register(r'reports', UserCourseStats)
router.register(r'lessons_user_progress', UserCourseLessonsStats)
router.register(r'course_stats', CourseStatsByLessonViewSet)
router.register(r'course_classes', ClassViewSet)
router.register(r'flatpage', FlatpageViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_view'),
    url(r'^courses', CoursesView.as_view(), name='courses'),

    # Uncomment the next line to enable the admin:
    url(r'^django/admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^django/admin/', include(django_admin.site.urls)),

    # Privileged browsing
    url(r'^admin/', include('administration.urls')),

    # Public browsing
    url(r'^my-courses/$', UserCoursesView.as_view(), name='user_courses'),
    url(r'^accept_terms/$', AcceptTermsView.as_view(), name='accept_terms'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)/intro/$', CourseView.as_view(), name='course_intro'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)/enroll/$', EnrollCourseView.as_view(), name='enroll_course'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)/resume/$', ResumeCourseView.as_view(), name='resume_course'),
    url(r'^course/(?P<course_slug>[-a-zA-Z0-9_]+)/lesson/(?P<slug>[-a-zA-Z0-9_]+)/$', LessonDetailView.as_view(), name='lesson'),
    url(r'^html5/', TemplateView.as_view(template_name="html5.html")),
    url(r'^empty/', TemplateView.as_view(template_name="empty.html")),
    url(r'^contact/?$', ContactView.as_view(), name="contact"),

    # Classes
    url(r'^course/(?P<course_slug>[-a-zA-Z0-9_]+)/classes/$', ClassListView.as_view(), name='classes'),
    url(r'^class/create/$', ClassCreateView.as_view(), name='class-create'),
    url(r'^class/(?P<pk>[0-9]+)/$', ClassUpdateView.as_view(), name='class'),
    url(r'^class/(?P<pk>[0-9]+)/delete/$', ClassDeleteView.as_view(), name='class-delete'),
    url(r'^class/(?P<pk>[0-9]+)/remove_user/$', ClassRemoveUserView.as_view(), name='class-remove-user'),
    url(r'^class/(?P<pk>[0-9]+)/add_users/$', ClassAddUsersView.as_view(), name='class-add-users'),


    # Services
    url(r'^api/', include(router.urls)),
    # Forum
    url(r'^forum/(?P<course_slug>[-a-zA-Z0-9_]+)/$', CourseForumView.as_view(), name='forum'),
    url(r'^forum/question/(?P<slug>[-a-zA-Z0-9_]+)/$', QuestionView.as_view(), name='forum_question'),
    url(r'^forum/question/add/(?P<course_slug>[-a-zA-Z0-9_]+)/$', QuestionCreateView.as_view(), name='forum_question_create'),
    url(r'^api/is_forum_moderator/(?P<course_id>[1-9][0-9]*)/$', ForumModeratorView.as_view(), name='is_forum_moderator'),

    # Course Material
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)/material/file_upload/$', FileUploadView.as_view(), name='file_upload'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)/material/$', CourseMaterialView.as_view(), name='course_material'),

    # Notes
    url(r'^notes/(?P<username>[\w.+-]+)?$', UserNotesView.as_view(), name='user_notes'),
    url(r'^course/(?P<course_slug>[-a-zA-Z0-9_]+)/mynotes/$', CourseNotesView.as_view(), name='user_course_notes'),

    # Messages
    url(r'^course/(?P<course_slug>[-a-zA-Z0-9_]+)/messages/$', GenericCourseView.as_view(template_name="messages.html"), name='messages'),
    url(r'^course/(?P<course_slug>[-a-zA-Z0-9_]+)/message/(?P<message_id>[1-9][0-9]*)$', GenericCourseView.as_view(template_name="message.html"), name='message_detail'),

    # Reports
    url(r'^course/(?P<course_slug>[-a-zA-Z0-9_]+)/reports/$', GenericCourseView.as_view(template_name="administration/stats.html"), name='reports'),

    # Authentication
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='timtec_logout'),

    url(r'^profile/edit/?$', ProfileEditView.as_view(), name="profile_edit"),
    url(r'^profile/(?P<username>[\w.+-]+)?/?$', ProfileView.as_view(), name="profile"),

    # The django-allauth
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/user_search/?$', UserSearchView.as_view(), name='user_search'),
    url(r'^api/student_search/?$', StudentSearchView.as_view(), name='student_search'),

    # The django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),

    url(r'^pages/', include('django.contrib.flatpages.urls')),

    url(r'^markdown/', include('django_markdown.urls')),

)

if settings.TWITTER_USER != '':
    from core.views import TwitterApi

    urlpatterns += (url(r'^api/twitter/?$', TwitterApi.as_view(), name='twitter'),)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'ifs' in settings.INSTALLED_APPS:
    urlpatterns += (url(r'^ifs/', include('ifs.urls')),)
