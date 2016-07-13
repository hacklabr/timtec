# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.views.generic import TemplateView
from accounts.views import (ProfileEditView, ProfileView, UserSearchView,
                            TimtecUserViewSet, TimtecUserAdminViewSet, StudentSearchView,
                            AcceptTermsView)

from core.views import (CourseView, GenericCourseView, CourseViewSet,
                        CourseProfessorViewSet, EnrollCourseView, HomeView,
                        UserCoursesView, ContactView, LessonDetailView,
                        LessonViewSet, StudentProgressViewSet,
                        UserNotesViewSet, CoursesView, CourseThumbViewSet,
                        ProfessorMessageViewSet, CourseStudentViewSet,
                        CarouselCourseView, ClassListView,
                        ClassCreateView, ClassUpdateView, ClassDeleteView,
                        ClassRemoveUserView, ClassAddUsersView, ClassViewSet,
                        ClassEvaluationsView,
                        FlatpageViewSet, CoursePictureUploadViewSet,
                        ResumeCourseView, FlatpageView, CourseAuthorViewSet,
                        CourseCertificationViewSet,
                        CourseCertificationDetailView,
                        CertificationProcessViewSet,
                        EvaluationViewSet, CertificateTemplateViewSet,
                        CertificateTemplateImageViewSet, RequestCertificateView,
                        EmitReceiptView, ProfileViewSet)

from activities.views import AnswerViewSet
from forum.views import (CourseForumView, QuestionView, QuestionCreateView, QuestionViewSet,
                         QuestionVoteViewSet, AnswerVoteViewSet, AnswerViewSet as ForumAnswerViewSet)
from course_material.views import CourseMaterialView, FileUploadView, CourseMaterialViewSet, CourseMaterialFileViewSet
from notes.views import NotesViewSet, CourseNotesView, UserNotesView
from reports.views import UserCourseStats, CourseStatsByLessonViewSet, UserCourseLessonsStats
from rest_framework import routers
from django_markdown import flatpages

# Uncomment the next two lines to enable the admin:
from django.contrib import admin as django_admin
django_admin.autodiscover()

flatpages.register()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', TimtecUserViewSet, base_name='user')
router.register(r'profile', ProfileViewSet, base_name='profile')
router.register(r'user_admin', TimtecUserAdminViewSet, base_name='user_admin')
router.register(r'course', CourseViewSet, base_name='course')
router.register(r'course_carousel', CarouselCourseView, base_name='course_carousel')
router.register(r'course_professor', CourseProfessorViewSet, base_name='course_professor')
router.register(r'course_professor_picture', CoursePictureUploadViewSet, base_name='course_professor_picture')
router.register(r'course_author', CourseAuthorViewSet, base_name='course_author')
router.register(r'course_student', CourseStudentViewSet, base_name='course_student')
router.register(r'professor_message', ProfessorMessageViewSet, base_name='professor_message')
router.register(r'coursethumbs', CourseThumbViewSet, base_name='coursethumbs')
router.register(r'lessons', LessonViewSet, base_name='lessons')
router.register(r'answer', AnswerViewSet, base_name='answer')
router.register(r'student_progress', StudentProgressViewSet, base_name='student_progress')
router.register(r'forum_question', QuestionViewSet, base_name='forum_question')
router.register(r'forum_answer', ForumAnswerViewSet, base_name='forum_answer')
router.register(r'question_vote', QuestionVoteViewSet, base_name='question_vote')
router.register(r'answer_vote', AnswerVoteViewSet, base_name='answer_vote')
router.register(r'course_material', CourseMaterialViewSet, base_name='course_material')
router.register(r'course_material_file', CourseMaterialFileViewSet, base_name='course_material_file')
router.register(r'note', NotesViewSet, base_name='note')
router.register(r'user_notes', UserNotesViewSet, base_name='user_notes')
router.register(r'reports', UserCourseStats, base_name='reports')
router.register(r'lessons_user_progress', UserCourseLessonsStats, base_name='lessons_user_progress')
router.register(r'course_stats', CourseStatsByLessonViewSet, base_name='course_stats')
router.register(r'course_classes', ClassViewSet, base_name='course_classes')
router.register(r'flatpage', FlatpageViewSet, base_name='flatpage')
router.register(r'course_certification', CourseCertificationViewSet, base_name='course_certification')
router.register(r'certification_process', CertificationProcessViewSet, base_name='certification_process')
router.register(r'evaluation', EvaluationViewSet, base_name='evaluation')
router.register(r'certificate_template', CertificateTemplateViewSet, base_name='certificate_template')
router.register(r'certificate_template_images', CertificateTemplateImageViewSet, base_name='certificate_template_images')

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

    url(r'^emit_recipt/(?P<course_id>[-a-zA-Z0-9_]+)$', EmitReceiptView.as_view(), name='emit_recipt'),
    url(r'^request_certificate/(?P<course_id>[-a-zA-Z0-9_]+)$',
        RequestCertificateView.as_view(),
        name='request_certificate'),

    url(r'^certificate/(?P<slug>[-a-zA-Z0-9_]+)/$', CourseCertificationDetailView.as_view(), name='certificate'),
    url(r'^certificate/(?P<slug>[-a-zA-Z0-9_]+)/print/$',
        CourseCertificationDetailView.as_view(template_name="certificate_print.html"),
        name='certificate-print'),
    url(r'^certificate/(?P<slug>[-a-zA-Z0-9_]+)/download/$', CourseCertificationDetailView.as_view(),
        name='certificate-download'),
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
    url(r'^class/(?P<pk>[0-9]+)/evaluations/$', ClassEvaluationsView.as_view(), name='class-evaluations'),

    # Evaluations
    url(r'^course/(?P<course_slug>[-a-zA-Z0-9_]+)/course_evaluations/$', GenericCourseView.as_view(template_name="course-evaluations.html"), name='course-evaluations'),

    # Services
    url(r'^api/', include(router.urls)),
    # Forum
    url(r'^forum/(?P<course_slug>[-a-zA-Z0-9_]+)/$', CourseForumView.as_view(), name='forum'),
    url(r'^forum/question/(?P<slug>[-a-zA-Z0-9_]+)/$', QuestionView.as_view(), name='forum_question'),
    url(r'^forum/question/add/(?P<course_slug>[-a-zA-Z0-9_]+)/$', QuestionCreateView.as_view(), name='forum_question_create'),

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

    url(r'^dashboard/', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    url(r'^dashboard/', TemplateView.as_view(template_name="dashboard.html")),
    url(r'^forum/', TemplateView.as_view(template_name="forum.html"), name='forum'),
    url(r'^thread/', TemplateView.as_view(template_name="forum-thread.html")),
    url(r'^login/', TemplateView.as_view(template_name="login.html")),
    url(r'^register/', TemplateView.as_view(template_name="register.html")),
    url(r'^flatpage/', TemplateView.as_view(template_name="flatpage.html")),

    url(r'^profile/edit/?$', ProfileEditView.as_view(), name="profile_edit"),
    url(r'^profile/(?P<username>[\w.+-]+)?/?$', ProfileView.as_view(), name="profile"),

    # The django-allauth
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/user_search/?$', UserSearchView.as_view(), name='user_search'),
    url(r'^api/student_search/?$', StudentSearchView.as_view(), name='student_search'),

    url(r'^pages(?P<url>.*)$', FlatpageView.as_view(), name='flatpage'),

    # The django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),

    url(r'^markdown/', include('django_markdown.urls')),

)

if settings.TWITTER_USER != '':
    from core.views import TwitterApi

    urlpatterns += (url(r'^api/twitter/?$', TwitterApi.as_view(), name='twitter'),)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'ifs' in settings.INSTALLED_APPS:
    urlpatterns += (url(r'^ifs/', include('ifs.urls')),)
