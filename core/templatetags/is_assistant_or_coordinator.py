from django import template

register = template.Library()


@register.filter()
def is_assistant_or_coordinator(user, course):
    return course.is_assistant_or_coordinator(user)
