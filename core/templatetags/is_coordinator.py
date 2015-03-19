from django import template
from core.models import CourseProfessor

register = template.Library()


@register.filter
def is_coordinator(user):
    return CourseProfessor.objects.filter(user=user, role='coordinator').exists()
