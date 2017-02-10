# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Django settings for timtec project.
from django.utils.translation import ugettext_lazy as _

import os


SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(SETTINGS_DIR)
APPS_DIR = PROJECT_ROOT

#
# Theme related options
#
THEMES_DIR = os.path.join(PROJECT_ROOT, 'themes')
TIMTEC_THEME = os.getenv('TIMTEC_THEME', 'default')  # don't forget to re run collectstatic if you change the theme

DEBUG = True
DEBUG = False

SITE_ID = 1
SITE_HOME = ''
SITE_NAME = u'TIM Tec'
SITE_DOMAIN = 'mooc.timtec.com.br'

ADMINS = (
    ('Admin1', 'root@localhost'),
)

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

PINAX_WEBANALYTICS_SETTINGS = {
    "google": {
        1: "set-your-google-analytics-key-here",
    },
}


LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "oauth2_provider.backends.OAuth2Backend",
)

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
    'compressor.finders.CompressorFinder',
)

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
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
)

ROOT_URLCONF = 'timtec.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'timtec.wsgi.application'


INSTALLED_APPS = (
    'django_extensions',
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
    'pinax.webanalytics',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.openid',
    'oauth2_provider',

    'django_markdown',

    'compressor',
    'localflavor',
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

COMPRESS_OFFLINE = True

COMPRESS_PRECOMPILERS = (
    ('text/less', '%s/node_modules/less/bin/lessc {infile} {outfile} --include-path="%s/less"' % (PROJECT_ROOT, STATIC_ROOT)),
)

try:
    execfile(os.path.join(SETTINGS_DIR, 'settings_local.py'))
except IOError:
    pass

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(THEMES_DIR, 'default', 'templates'),
        ],
        'OPTIONS': {
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
            'loaders': [
                'core.loaders.TimtecThemeLoader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.filesystem.Loader',
            ],
        },
    },
]

# Additional locations of static files
STATICFILES_DIRS = ()

if TIMTEC_THEME not in INSTALLED_APPS:
    STATICFILES_DIRS += (
        os.path.join(THEMES_DIR, TIMTEC_THEME, 'static'),
    )

STATICFILES_DIRS += (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(THEMES_DIR, 'default', 'static'),
    os.path.join(PROJECT_ROOT, 'bower_components'),
)

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'openid': 'Openid scope',
    },
}

# Fix debug toolbar issue: https://github.com/django-debug-toolbar/django-debug-toolbar/issues/521
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
