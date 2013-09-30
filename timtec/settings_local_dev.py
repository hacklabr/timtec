# configurations for the staging server
# https://docs.djangoproject.com/en/dev/ref/settings/
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'timtec-dev.hacklab.com.br',
    '.timtec.com.br',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_SUBJECT_PREFIX = '[timtec-staging]'
DEFAULT_FROM_EMAIL = 'timtec-staging@timtec.com.br'

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
