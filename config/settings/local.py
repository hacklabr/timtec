# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""
from .common import *  # noqa

# whyyy
AUTOSLUG_SLUGIFY_FUNCTION='django.utils.text.slugify'

# TIMTec
# ------------------------------------------------------------------------------
# TIMTEC_THEME = 'timtec'
# TIMTEC_THEME = 'ifs-colors'
TIMTEC_THEME = 'base'
# TIMTEC_THEME = env('TIMTEC_THEME', default='default')


# INSTALLED_APPS += ("my_theme", )

# DEBUG
# ------------------------------------------------------------------------------
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='u%#grp^d)o74t7z!q(lved(djeah4@5l!uq9i*bfa0ku-@y&=h')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings

SITE_DOMAIN = env('DJANGO_SITE_DOMAIN', default=env('VIRTUAL_HOST', default='localhost'))
SITE_NAME = env('DJANGO_SITE_NAME', default='TIM Tec')
DOMAIN_NAME = SITE_DOMAIN

DEFAULT_FROM_EMAIL = env.list('DEFAULT_FROM_EMAIL', default='donotreply@' + DOMAIN_NAME)

SITE_ID = env.int('DJANGO_SITE_ID', 1)
TIME_ZONE = env('DJANGO_TIME_ZONE', default='America/Sao_Paulo')
LANGUAGE_CODE = env('DJANGO_LANGUAGE_CODE', default='pt-br')

INSTALLED_APPS += env.tuple('DJANGO_INSTALLED_APPS', default=())
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

METRON_SETTINGS = {
    "google": {
        SITE_ID: env('GOOGLE_ANALYTICS', default=""), # UA-XXXXXXXX-X
    },
}

if env('OPENID', default=None):
    SOCIALACCOUNT_PROVIDERS['openid'] = {
        'SERVERS': [
            env.dict('OPENID')
        ]
    }

MEDIA_ROOT = env('DJANGO_MEDIA_ROOT', default=MEDIA_ROOT)
STATIC_ROOT = env('DJANGO_STATIC_ROOT', default=STATIC_ROOT)

vars().update(env.email_url('EMAIL_URL', default='consolemail://'))

TERMS_ACCEPTANCE_REQUIRED = env.bool('TERMS_ACCEPTANCE_REQUIRED', default=False)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}
