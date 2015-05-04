# -*- coding: utf-8 -*-
# configurations for the production server
# https://docs.djangoproject.com/en/dev/ref/settings/
DEBUG = False
TEMPLATE_DEBUG = DEBUG

TIMTEC_THEME = 'ifs-colors'

SITE_ID = 2
SITE_NAME = 'IFSUL'

ALLOWED_HOSTS = [
    'ifsul.timtec.com.br',
    '.ifsul.timtec.com.br',
    'ifsul.hacklab.com.br',
    '.ifsul.hacklab.com.br',
    'mooc.ifsul.edu.br',
    '.mooc.ifsul.edu.br',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec-ifsul',
        'USER': 'timtec-ifsul',
    }
}

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.insert(INSTALLED_APPS.index('accounts') + 1, 'ifs')

ACCOUNT_SIGNUP_FORM_CLASS = 'ifs.forms.IfSignupForm'
AUTH_USER_MODEL = 'ifs.IfUser'
ACCOUNT_FORMS = {'login': 'ifs.forms.IfLoginForm'}

MEDIA_ROOT = "/home/timtec-ifsul/webfiles/media/"
STATIC_ROOT = "/home/timtec-ifsul/webfiles/static/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[ifsul]'
DEFAULT_FROM_EMAIL = 'donotreply@m.timtec.com.br'
CONTACT_RECIPIENT_LIST = ['mooc@ifsul.edu.br', ]

TERMS_ACCEPTANCE_REQUIRED = False

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
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/home/timtec-ifsul/django.log',
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
