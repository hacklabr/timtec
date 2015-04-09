# -*- coding: utf-8 -*-
# configurations for the design server
# https://docs.djangoproject.com/en/dev/ref/settings/
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
SITE_NAME = u'Marca da instituição'
ALLOWED_HOSTS = [
    'design.hacklab.com.br',
    '.timtec.com.br',
]

TIMTEC_THEME = 'new-if'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'timtec-design',
        'USER': 'timtec-design',
    }
}

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.insert(INSTALLED_APPS.index('accounts') + 1, 'ifs')

ACCOUNT_SIGNUP_FORM_CLASS = 'ifs.forms.IfSignupForm'
AUTH_USER_MODEL = 'ifs.IfUser'
ACCOUNT_FORMS = {'login': 'ifs.forms.IfLoginForm'}

MEDIA_ROOT = "/home/timtec-design/webfiles/media/"
STATIC_ROOT = "/home/timtec-design/webfiles/static/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_SUBJECT_PREFIX = '[timtec-design]'
DEFAULT_FROM_EMAIL = 'timtec-design@timtec.com.br'
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
