# -*- coding: utf-8 -*-
from core.forms import ContactForm
from django.conf import settings


def contact_form(request):
    return {'contact_form': ContactForm()}


def site_settings(request):
    return {'site': {'domain': settings.SITE_DOMAIN,
                     'home': settings.SITE_HOME,
                     'name': settings.SITE_NAME,
                     'YOUTUBE_API_KEY': settings.YOUTUBE_API_KEY}}


def get_current_path(request):

    return {'current_path': request.get_full_path()}


def terms_acceptance_required(request):
    return {'terms_required': settings.TERMS_ACCEPTANCE_REQUIRED}
