from django import template
from core.models import StudentProgress

register = template.Library()

@register.filter(name='status')
def status(value, user):
    if user.id:
        if StudentProgress.objects.filter(unit=value, user=user).exclude(complete=None):
            return 'done'
    return ''