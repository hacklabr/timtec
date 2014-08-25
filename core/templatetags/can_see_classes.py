from django import template

register = template.Library()


@register.filter()
def can_see_classes(user, course):
    return course.has_perm_own_classes(user)
