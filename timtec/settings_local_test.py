# -*- coding: utf-8 -*-
# configurations for the test server
# https://docs.djangoproject.com/en/dev/ref/settings/
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

ALLOWED_HOSTS = [
    'timtec-test.hacklab.com.br',
    '.timtec.com.br',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec-test',
        'USER': 'timtec-test',
    }
}

MEDIA_ROOT = "/home/timtec-test/webfiles/media/"
STATIC_ROOT = "/home/timtec-test/webfiles/static/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[timtec-test]'
DEFAULT_FROM_EMAIL = 'donotreply-test@m.timtec.com.br'
CONTACT_RECIPIENT_LIST = ['timtec-dev@listas.hacklab.com.br', ]

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
