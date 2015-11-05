# -*- coding: utf-8 -*-
# configurations for the design server
# https://docs.djangoproject.com/en/dev/ref/settings/
DEBUG = False
TEMPLATE_DEBUG = DEBUG

TIMTEC_THEME = 'ifs-colors'

SITE_ID = 2
SITE_NAME = 'Marca da instituição'
ALLOWED_HOSTS = [
    'demo.hacklab.com.br',
    '.timtec.com.br',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec-demo',
        'USER': 'timtec-demo',
    }
}
#
# ACCOUNT_SIGNUP_FORM_CLASS = 'ifs.forms.IfSignupForm'
# AUTH_USER_MODEL = 'ifs.IfUser'
# ACCOUNT_FORMS = {'login': 'ifs.forms.IfLoginForm'}
# INSTALLED_APPS = list(INSTALLED_APPS)
# INSTALLED_APPS.insert(INSTALLED_APPS.index('accounts') + 1, 'ifs')

MEDIA_ROOT = "/home/timtec-demo/webfiles/media/"
STATIC_ROOT = "/home/timtec-demo/webfiles/static/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_SUBJECT_PREFIX = '[timtec-demo]'
DEFAULT_FROM_EMAIL = 'donotreply@m.timtec.com.br'
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
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
