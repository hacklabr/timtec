from django import template

register = template.Library()


@register.filter()
def is_course_coordinator(user, course):
    return course.is_course_coordinator(user)
