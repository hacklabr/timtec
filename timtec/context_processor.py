from django.utils.translation import to_locale, get_language
from django.conf import settings


def locale(request):
    return {'LOCALE': to_locale(get_language())}


def openid_providers(request):
    providers = getattr(settings, 'SOCIALACCOUNT_PROVIDERS', {})
    openid = providers.get('openid', {})
    servers = openid.get('SERVERS', [])
    return {'openid_providers': servers}
