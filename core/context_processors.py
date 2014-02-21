# -*- coding: utf-8 -*-
from core.forms import ContactForm
from django.conf import settings


def contact_form(request):
    return {'contact_form': ContactForm()}


def site_settings(request):
    return {'site': {'domain': settings.SITE_DOMAIN,
                     'home': settings.SITE_HOME,
                     'name': settings.SITE_NAME}}
