from django import template

register = template.Library()


@register.filter()
def is_enrolled(user, course):
    return course.is_enrolled(user)
