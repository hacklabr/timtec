from django import template

register = template.Library()


@register.filter()
def is_enrolled(user, course):
    if user.is_anonymous():
        return False
    return course.is_enrolled(user)
