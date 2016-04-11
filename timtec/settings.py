# -*- coding: utf-8 -*-
# Django settings for timtec project.
from django.utils.translation import ugettext_lazy as _

import os


SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(SETTINGS_DIR)

#
# Theme related options
#
THEMES_DIR = os.path.join(PROJECT_ROOT, 'themes')
TIMTEC_THEME = os.getenv('TIMTEC_THEME', 'default')  # don't forget to re run collectstatic if you change the theme

SOUTH_AUTO_FREEZE_APP = True

DEBUG = True

SITE_ID = 1
SITE_HOME = ''
SITE_NAME = u'TIM Tec'
SITE_DOMAIN = 'mooc.timtec.com.br'

ADMINS = (
    ('Admin1', 'root@localhost'),
    ('timtec-dev list', 'timtec-dev@listas.hacklab.com.br'),
)

MANAGERS = (ADMINS[1],)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'donotreply-dev@m.timtec.com.br'
CONTACT_RECIPIENT_LIST = ['timtec-dev@listas.hacklab.com.br', ]

TERMS_ACCEPTANCE_REQUIRED = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec',
    }
}

METRON_SETTINGS = {
    "google": {
        1: "set-your-google-analytics-key-here",
    },
}


LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",
                           "allauth.account.auth_backends.AuthenticationBackend")

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

LANGUAGES = (
    ('pt-br', _('Brazilian Portuguese')),
    ('it', _('Italian')),
    ('es', _('Spanish')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)


# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'pipeline.finders.FileSystemFinder',
    # 'pipeline.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# PIPELINE_ENABLED = True
PIPELINE_YUGLIFY_BINARY = os.path.join(PROJECT_ROOT, 'node_modules', 'yuglify', 'bin', 'yuglify')
PIPELINE_UGLIFYJS_BINARY = os.path.join(PROJECT_ROOT, 'node_modules', 'uglify-js', 'bin', 'uglifyjs')
PIPELINE_NGANNOTATE_BINARY = os.path.join(PROJECT_ROOT, 'node_modules', 'ng-annotate', 'build', 'es5', 'ng-annotate')

PIPELINE_JS_COMPRESSOR = 'timtec.ngmincombo.NgminComboCompressor'

PIPELINE_LESS_BINARY = os.path.join(PROJECT_ROOT, 'node_modules', 'less', 'bin', 'lessc')

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

# Source Map Less
PIPELINE_LESS_ARGUMENTS = '--source-map=main.css.map'

PIPELINE_CSS = {
    'common': {
        'source_filenames': (
            'font-awesome/css/font-awesome.css',
            'codemirror/lib/codemirror.css',
            'codemirror/addon/hint/show-hint.css',
            'codemirror/theme/monokai.css',
            'css/codemirrorconf.css',
            'intro.js/introjs.css',
            'intro.js/themes/introjs-nassim.css',
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
}

PIPELINE_JS = {
    'all': {
        'source_filenames': (
            'modernizr/modernizr.js',
            'jquery/dist/jquery.js',
            'jquery-ui/ui/jquery-ui.js',
            'jquery-ui/ui/jquery.ui.sortable.js',
            'bootstrap/dist/js/bootstrap.js',
            'angular/angular.js',
            'angular-animate/angular-animate.js',
            'angular-cookies/angular-cookies.js',
            'angular-resource/angular-resource.js',
            'angular-route/angular-route.js',
            'angular-sanitize/angular-sanitize.js',
            'angular-bootstrap/ui-bootstrap-tpls.js',
            'bootstrap-ui-datetime-picker/dist/datetime-picker.min.js',
            'angular-gettext/dist/angular-gettext.js',
            'angular-i18n/angular-locale_pt-br.js',
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

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e%6a01vfbue28$xxssu!9r_)usqjh817((mr+7vv3ek&@#p0!$'

# Django Suit configuration example
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Timtec Admin',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    'SEARCH_URL': '/admin/accounts/timtecuser/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    #     'sites',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('accounts.TimtecUser', 'auth.group')},
    #     # {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    # 'LIST_PER_PAGE': 15
}

AUTH_USER_MODEL = 'accounts.TimtecUser'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'timtec.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'timtec.wsgi.application'


INSTALLED_APPS = (
    'django_extensions',
    'pipeline',
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'rest_framework',
    'rosetta',
    'autoslug',
    # TIM Tec
    'accounts',
    'activities',
    'administration',
    'forum',
    'course_material',
    'notes',
    'reports',
    'core',
    # django-metron
    'metron',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.openid',

    'django_markdown',

    # raven has to be the last one
    'raven.contrib.django.raven_compat',
)


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
PHANTOMJS_PATH = os.path.join(PROJECT_ROOT, 'node_modules/phantomjs-prebuilt/bin/phantomjs')

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
TWITTER_ACESS_TOKEN = ''
TWITTER_ACESS_TOKEN_SECRET = ''
TWITTER_USER = ''

YOUTUBE_API_KEY = ''
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    execfile(os.path.join(SETTINGS_DIR, 'settings_local.py'))
except IOError:
    pass

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(THEMES_DIR, TIMTEC_THEME, 'templates'),
            os.path.join(THEMES_DIR, 'default', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
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
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'core.loaders.TimtecThemeLoader',
            ],
            'debug': DEBUG,
        },
    },
]

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(THEMES_DIR, TIMTEC_THEME, 'static'),
    os.path.join(THEMES_DIR, 'default', 'static'),
    os.path.join(PROJECT_ROOT, 'bower_components'),
)

if DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1', )

# Fix debug toolbar issue: https://github.com/django-debug-toolbar/django-debug-toolbar/issues/521
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
