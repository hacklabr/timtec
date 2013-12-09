# -*- coding: utf-8 -*-
# Django settings for timtec project.
import os
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(SETTINGS_DIR)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

ADMINS = (
    ('Admin1', 'root@localhost'),
    ('timtec-dev list', 'timtec-dev@listas.hacklab.com.br'),
)

MANAGERS = (ADMINS[1],)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'donotreply-dev@m.timtec.com.br'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'timtec.sqlite',                # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}


METRON_SETTINGS = {
    "google": {
        1: "set-your-google-analytics-key-here",
    },
}


LOGIN_URL = '/login/'

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
    ('pt-br', u'Português'),
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
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "static"),
    os.path.join(PROJECT_ROOT, 'bower_components'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'pipeline.finders.FileSystemFinder',
    'pipeline.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.CachedFileFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
    'common': {
        'source_filenames': (
            'fonts/teuton/stylesheet.css',
            'fonts/questrial/stylesheet.css',
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
    'admin': {
        'source_filenames': (
            'css/main-admin.less',
        ),
        'output_filename': 'css/admin.css',
        'extra_context': {
            'media': 'screen,projection,print',
        },
    },
}

PIPELINE_JS = {
    'all': {
        'source_filenames': (
            'modernizr/modernizr.js',
            'jquery/jquery.js',
            'bootstrap/dist/js/bootstrap.js',
            'angular/angular.js',
            'angular-animate/angular-animate.js',
            'angular-cookies/angular-cookies.js',
            'angular-resource/angular-resource.js',
            'angular-route/angular-route.js',
            'angular-sanitize/angular-sanitize.js',
            # 'angular-ui-codemirror/angular-ui-codemirror.js',
            'js/contact_form.js',
            'js/helpers.js',
            'js/angular-youtube.js',
        ),
        'output_filename': 'js/all.js',
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
            'js/codemirrorconf.js',
        ),
        'output_filename': 'js/codemirrorcomp.js',
    }
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
}

APPEND_SLASH = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e%6a01vfbue28$xxssu!9r_)usqjh817((mr+7vv3ek&@#p0!$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SETTINGS_DIR, 'templates'),
)


from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'core.context_processors.contact_form',
)

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
    'django.middleware.locale.LocaleMiddleware',
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
    'south',
    'pipeline',
    'suit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'rest_framework',
    'rosetta',
    'autoslug',
    # TIM Tec
    'core',
    'accounts',
    'activities',
    'administration',
    'forum',
    'course_material',
    'notes',
    # django-metron
    'metron',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    # raven has to be the last one
    'raven.contrib.django.raven_compat',
)


SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
    }
}

if DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1', )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }


# django-registration flag
# ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_DEFAULT_GROUP_NAME = 'students'
ACCOUNT_ADAPTER = "accounts.adapter.TimtecAdapter"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[timtec] "
SOCIALACCOUNT_EMAIL_VERIFICATION = False

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
    from .settings_local import *
except ImportError:
    pass
