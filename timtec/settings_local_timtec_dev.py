# -*- coding: utf-8 -*-
# configurations for the dev server
# https://docs.djangoproject.com/en/dev/ref/settings/
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_PATCH_SETTINGS = False

SITE_ID = 1

ALLOWED_HOSTS = [
    'timtec-dev.hacklab.com.br',
    '.timtec.com.br',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec-dev',
        'USER': 'timtec-dev',
    }
}

# Needed in ubuntu 14.04 instalations
PIPELINE_LESS_BINARY = '/usr/local/bin/lessc'

MEDIA_ROOT = "/home/timtec-dev/webfiles/media/"
STATIC_ROOT = "/home/timtec-dev/webfiles/static/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_SUBJECT_PREFIX = '[timtec-dev]'
DEFAULT_FROM_EMAIL = 'timtec-dev@timtec.com.br'
CONTACT_RECIPIENT_LIST = ['timtec-dev@listas.hacklab.com.br', ]

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
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/timtec-dev/django-dev.log',
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
