# -*- coding: utf-8 -*-
# configurations for the staging server
# https://docs.djangoproject.com/en/dev/ref/settings/

import os.path
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(SETTINGS_DIR)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

ALLOWED_HOSTS = [
    'timtec-dev.hacklab.com.br',
    '.timtec.com.br',
    'localhost'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec',
    }
}


MEDIA_ROOT = "/home/timtec-dev/webfiles/media/"
STATIC_ROOT = "/home/timtec-dev/webfiles/static/"
# MEDIA_URL = 'http://localhost:8002/media/'

# STATIC_URL = 'http://localhost:8002/static/'

EMAIL_SUBJECT_PREFIX = '[timtec-dev]'

# MEDIA_ROOT = os.path.join(PROJECT_ROOT, '../webfiles/media/')
# STATIC_ROOT = os.path.join(PROJECT_ROOT, '../webfiles/static/')


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
