from rest_framework import permissions


class HideQuestionPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user in obj.course.professors.all():
            return True
        elif request.user.groups.filter(name="professors"):
            # FIXME remove this after implement tutor professor
            return True
