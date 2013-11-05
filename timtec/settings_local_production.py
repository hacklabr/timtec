# configurations for the production server
# https://docs.djangoproject.com/en/dev/ref/settings/
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2

ALLOWED_HOSTS = [
    'timtec.com.br',
    '.timtec.com.br',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec-production',
        'USER': 'timtec-production',
    }
}

MEDIA_ROOT = "/home/timtec-production/webfiles/media/"
STATIC_ROOT = "/home/timtec-production/webfiles/static/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_SUBJECT_PREFIX = '[timtec]'
DEFAULT_FROM_EMAIL = 'timtec@timtec.com.br'

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
