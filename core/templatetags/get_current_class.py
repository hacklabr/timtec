from django import template
from django.core.exceptions import ObjectDoesNotExist


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_current_class(context, course):

    current_user = context.get('user')
    if current_user.is_anonymous():
        return None
    current_class = None

    try:
        current_class = course.class_set.get(students=current_user)
    except ObjectDoesNotExist:
        pass

    # If user is not student in any class in this course, verify if it is professor
    # import ipdb;ipdb.set_trace()
    if not current_class:
        try:
            current_class = current_user.professor_classes.get(course=course)
        except ObjectDoesNotExist:
            pass

    return current_class
