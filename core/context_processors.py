# -*- coding: utf-8 -*-
from core.forms import ContactForm


def contact_form(request):
    return {'contact_form': ContactForm()}
