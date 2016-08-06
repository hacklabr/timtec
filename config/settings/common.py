# -*- coding: utf-8 -*-
"""
Django settings for timtec project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals
from django.utils.translation import ugettext_lazy as _

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (timtec/config/settings/common.py - 3 = timtec/)
# APPS_DIR = ROOT_DIR.path('timtec')
APPS_DIR = ROOT_DIR

env = environ.Env()

# Theme related options
# -----------------------------------------------------------------------
THEMES_DIR = APPS_DIR.path('themes')
TIMTEC_THEME = env('TIMTEC_THEME', default='default')

# THEMES_DIR = os.path.join(PROJECT_ROOT, 'themes')
# don't forget to re run collectstatic if you change the theme
# TIMTEC_THEME = os.getenv('TIMTEC_THEME', 'default')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'suit',
    'django_extensions',
    'pipeline',
    'rest_framework',
    'rosetta',
    #'autoslug',

    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.openid',

    'django_markdown',
    'metron',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'accounts',
    'activities',
    'administration',
    'forum',
    'course_material',
    'notes',
    'reports',
    'core',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
# FIXME: check this
# MIGRATION_MODULES = {
#     'sites': 'timtec.contrib.sites.migrations'
# }

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Admin""", 'root@localhost'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db('DJANGO_DATABASE_URL', default='postgres://localhost/timtec'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'pt-br'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

LANGUAGES = (
    ('pt-br', _('Brazilian Portuguese')),
    ('it', _('Italian')),
    ('es', _('Spanish')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    str(ROOT_DIR.path('locale')),
)

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(THEMES_DIR.path('default', 'templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'core.loaders.TimtecThemeLoader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # TIMTec context_processors
                'core.context_processors.contact_form',
                'core.context_processors.site_settings',
                'core.context_processors.get_current_path',
                'core.context_processors.terms_acceptance_required',
                'timtec.context_processor.locale',
                'timtec.context_processor.openid_providers',
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = ()

if TIMTEC_THEME not in INSTALLED_APPS:
    STATICFILES_DIRS += (
        str(THEMES_DIR.path(TIMTEC_THEME, 'static')),
    )

STATICFILES_DIRS += (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    str(THEMES_DIR.path('default', 'static')),
    str(ROOT_DIR.path('bower_components')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'pipeline.finders.FileSystemFinder',
    # 'pipeline.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',

    'compressor.finders.CompressorFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE = {
    'COMPILERS': (
        'pipeline.compilers.less.LessCompiler',
        'pipeline.compilers.sass.SASSCompiler',
    ),
    'YUGLIFY_BINARY': str(ROOT_DIR.path('node_modules', 'yuglify', 'bin', 'yuglify')),
    'UGLIFYJS_BINARY': str(ROOT_DIR.path('node_modules', 'uglify-js', 'bin', 'uglifyjs')),

    'NGANNOTATE_BINARY': str(ROOT_DIR.path('node_modules', 'ng-annotate', 'build', 'es5', 'ng-annotate')),
    'NGANNOTATE_ARGUMENTS': ' -a - ',

    'LESS_BINARY': str(ROOT_DIR.path('node_modules', 'less', 'bin', 'lessc')),
    'LESS_ARGUMENTS': '--source-map=main.css.map',

    'SASS_BINARY': str(ROOT_DIR.path('node_modules', 'node-sass', 'bin', 'node-sass')),
    'SASS_ARGUMENTS': '--source-map true',
    #  '--source-map-contents sass --include-path'
    'SHOW_ERRORS_INLINE': False,
    'JS_COMPRESSOR': 'timtec.ngmincombo.NgminComboCompressor',

    'STYLESHEETS': {
        'common': {
            'source_filenames': (
                'font-awesome/css/font-awesome.css',
                'codemirror/lib/codemirror.css',
                'codemirror/addon/hint/show-hint.css',
                'codemirror/theme/monokai.css',
                'css/codemirrorconf.css',
            ),
            'output_filename': 'css/common.css',
            'extra_context': {
                'media': 'screen,projection,print',
            },
        },
        'public': {
            'source_filenames': (
                'css/main.less',
            ),
            'output_filename': 'css/public.css',
            'extra_context': {
                'media': 'screen,projection,print',
            },
        },
    },

    'JAVASCRIPT': {
        'all': {
            'source_filenames': (
                'modernizr/modernizr.js',
                'jquery/dist/jquery.js',
                'jquery-ui/ui/jquery-ui.js',
                'jquery-ui/ui/jquery.ui.sortable.js',
                'bootstrap/dist/js/bootstrap.js',
                'intro.js/intro.js',
                'js/consolelogfallback.js',
                'js/django.js',
                'js/contact_form.js',
                'js/helpers.js',
                'js/angular-youtube.js',
                'js/truncate.js',
                'js/layout.js',
            ),
            'output_filename': 'js/all.js',
        },
        'angular-commons': {
            'source_filenames': (
                'angular/angular.js',
                'angular-animate/angular-animate.js',
                'angular-cookies/angular-cookies.js',
                'angular-resource/angular-resource.js',
                'angular-route/angular-route.js',
                'angular-sanitize/angular-sanitize.js',
                'angular-bootstrap/ui-bootstrap-tpls.js',
                'angular-gettext/dist/angular-gettext.js',
                'angular-i18n/angular-locale_pt-br.js'
            ),
            'output_filename': 'js/angular-commons.js',
        },
        'markdown': {
            'source_filenames': (
                'js/vendor/pagedown/Markdown.Converter.js',
                'js/vendor/pagedown/Markdown.Editor.js',
                'js/vendor/pagedown/Markdown.Sanitizer.js',
                'js/markdown/app.js',
                'js/markdown/filters.js',
            ),
            'output_filename': 'js/markdown.js',
        },
        'messages': {
            'source_filenames': (
                'js/messages/app.js',
                'js/messages/controllers.js',
                'js/messages/services.js',
                'checklist-model/checklist-model.js',
                'js/markdown/app.js',
                'js/markdown/filters.js',
                'js/factories/timtec-models.js',
            ),
            'output_filename': 'js/messages.js',
        },
        'certificate': {
            'source_filenames': (
                'js/certificate/app.js',
                'js/certificate/controllers.js',
                'js/certificate/filters.js',
                'js/certificate/services.js',
                'checklist-model/checklist-model.js',
                'js/directives/file.js',
                'js/directives/previewImage.js',
                'js/directives/alertPopup.js',
                'js/directives/fixedBar.js',
                'js/factories/timtec-models.js',
            ),
            'output_filename': 'js/certificate.js',
        },
        'codemirror': {
            'source_filenames': (
                'codemirror/lib/codemirror.js',
                'codemirror/addon/fold/xml-fold.js',
                'codemirror/addon/hint/show-hint.js',
                'codemirror/addon/hint/xml-hint.js',
                'codemirror/addon/hint/html-hint.js',
                'codemirror/addon/hint/css-hint.js',
                'codemirror/addon/hint/javascript-hint.js',
                'codemirror/addon/edit/matchbrackets.js',
                'codemirror/addon/edit/closebrackets.js',
                'codemirror/addon/edit/matchtags.js',
                'codemirror/mode/xml/xml.js',
                'codemirror/mode/css/css.js',
                'codemirror/mode/javascript/javascript.js',
                'codemirror/mode/htmlmixed/htmlmixed.js',
                'codemirror/mode/clike/clike.js',
                'codemirror/mode/php/php.js',
                # 'js/codemirrorconf.js',
                'js/vendor/angular-ui-codemirror/ui-codemirror.js',
            ),
            'output_filename': 'js/codemirrorcomp.js',
        },
        'markdown_editor': {
            'source_filenames': (
                'js/vendor/pagedown/Markdown.Converter.js',
                'js/vendor/pagedown/Markdown.Editor.js',
                'js/vendor/pagedown/Markdown.Sanitizer.js',
            ),
            'output_filename': 'js/markdown_editor.js',
        },
        'lesson': {
            'source_filenames': (
                'js/activities/app.js',
                'js/activities/controllers.js',
                'js/activities/directives.js',
                'js/activities/services.js',
                'js/lesson/app.js',
                'js/lesson/controllers.js',
                'js/lesson/services.js',
                'js/directives/markdowneditor.js',
                'js/directives/codemirror.js',
                'js/directives/layout.js',
            ),
            'output_filename': 'js/lesson.js',
        },
        'course_material': {
            'source_filenames': (
                'js/course_material/app.js',
                'js/course_material/controllers.js',
                'js/course_material/services.js',
                'js/course_material/directives.js',
                'js/course_material/filters.js',
                'js/directives/markdowneditor.js',
                'dropzone/downloads/dropzone.js',
                'angular-dropzone/lib/angular-dropzone.js',
                'js/directives/alertPopup.js',
                'js/directives/fixedBar.js',
            ),
            'output_filename': 'js/course_material.js',
        },
        'forum': {
            'source_filenames': (
                'js/forum/app.js',
                'js/forum/controllers.js',
                'js/forum/directives.js',
                'js/forum/filters.js',
                'js/forum/services.js',
                'js/truncate.js',
                'js/factories/timtec-models.js',
            ),
            'output_filename': 'js/forum.js',
        },
        'notes': {
            'source_filenames': (
                'js/notes/app.js',
                'js/notes/controllers.js',
                'js/notes/services.js',
            ),
            'output_filename': 'js/notes.js',
        },
        'reports': {
            'source_filenames': (
                'js/reports/app.js',
                'js/reports/controllers.js',
                'js/reports/services.js',
                'js/factories/timtec-models.js',
            ),
            'output_filename': 'js/reports.js',
        },
        'core': {
            'source_filenames': (
                'js/core/app.js',
                'js/core/controllers.js',
                'js/core/services.js',
                'js/core/filters.js',
                'angular-tweet-filter/index.js',
                'angular-sortable-view/src/angular-sortable-view.min.js',
                'js/directives/fixedBar.js',
                'js/directives/alertPopup.js',
                'js/directives/markdowneditor.js',
            ),
            'output_filename': 'js/core.js',
        },
        'course_permissions': {
            'source_filenames': (
                'js/course-permissions/app.js',
                'js/course-permissions/controllers.js',
                'js/factories/timtec-models.js',
                'js/directives/fixedBar.js',
                'js/directives/alertPopup.js',
            ),
            'output_filename': 'js/course_permissions.js',
        },
        'users_admin': {
            'source_filenames': (
                'js/users-admin/app.js',
                'js/users-admin/controllers.js',
                'js/users-admin/services.js',
                'js/factories/timtec-models.js',
                'js/directives/fixedBar.js',
                'js/directives/alertPopup.js',
            ),
            'output_filename': 'js/users_admin.js',
        },
    }
}

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'timtec.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Some really nice defaults
# ACCOUNT_AUTHENTICATION_METHOD = 'username'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
#
# ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
# ACCOUNT_ADAPTER = 'timtec.users.adapters.AccountAdapter'
# SOCIALACCOUNT_ADAPTER = 'timtec.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
# AUTH_USER_MODEL = 'users.User'
# LOGIN_REDIRECT_URL = 'users:redirect'
# LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^django/admin/'

MOMMY_CUSTOM_FIELDS_GEN = {
    'jsonfield.JSONField': lambda: '{}',
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ],

    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

APPEND_SLASH = True

AUTH_USER_MODEL = 'accounts.TimtecUser'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'METHOD': 'oauth2',
        'VERSION': 'v2.2',
    },
}

# django-registration flag
# ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_DEFAULT_GROUP_NAME = 'students'
ACCOUNT_ADAPTER = "accounts.adapter.TimtecAdapter"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[timtec] "
ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.SignupForm'
ACCOUNT_REQUIRED_FIELDS = ('first_name', 'last_name', )
SOCIALACCOUNT_EMAIL_VERIFICATION = False

CERTIFICATE_SIZE = (862, 596)
PHANTOMJS_PATH = str(ROOT_DIR.path('node_modules/phantomjs-prebuilt/bin/phantomjs'))

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACESS_TOKEN = ''
TWITTER_ACESS_TOKEN_SECRET = ''
TWITTER_USER = ''

YOUTUBE_API_KEY = ''

# FIXME remove these
SITE_HOME = ''
SITE_NAME = u'TIM Tec'
SITE_DOMAIN = 'localhost'
