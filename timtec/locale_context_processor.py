from django.utils.translation import to_locale, get_language


def locale(request):
    return {'LOCALE': to_locale(get_language())}
