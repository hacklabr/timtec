from django import template

register = template.Library()


@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
