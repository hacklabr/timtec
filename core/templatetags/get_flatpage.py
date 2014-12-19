from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import get_current_site


register = template.Library()


class FlatpageNode(template.Node):
    def __init__(self, context_name, url):
        self.context_name = context_name
        self.url = template.Variable(url)

    def render(self, context):
        if 'request' in context:
            site_pk = get_current_site(context['request']).pk
        else:
            site_pk = settings.SITE_ID
        try:
            flatpage = FlatPage.objects.get(sites__id=site_pk, url=self.url.resolve(context))
        except ObjectDoesNotExist:
            flatpage = FlatPage(url=self.url.resolve(context))

        context[self.context_name] = flatpage
        return ''


@register.tag
def get_flatpage(parser, token):
    """
    Retrieves the flatpage object for the specified url
    Syntax::
        {% get_flatpages ['url'] as context_name %}
    Example usage::
        {% get_flatpages '/about/' as about_page %}
    """
    bits = token.split_contents()
    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "['url'] as context_name" %
                      dict(tag_name=bits[0]))
    # Must have at 3-6 bits in the tag
    if len(bits) == 4:

        # The very last bit must be the context name
        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        context_name = bits[-1]

        url = bits[1]

        return FlatpageNode(context_name, url)
    else:
        raise template.TemplateSyntaxError(syntax_message)
