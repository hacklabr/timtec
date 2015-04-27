from rest_framework import permissions
from core.models import Course, CourseProfessor, CourseAuthor


class IsProfessorCoordinatorOrAdminPermissionOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow course coordinator edit Course and CourseProfessors objects instances
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_superuser:
            return True
        elif request.user.is_authenticated() and isinstance(obj, CourseProfessor) and obj.course.get_professor_role(request.user) == 'coordinator':
            return True
        elif request.user.is_authenticated() and isinstance(obj, Course) and obj.get_professor_role(request.user) == 'coordinator':
            return True
        elif request.user.is_authenticated() and isinstance(obj, CourseAuthor) and obj.course.get_professor_role(request.user) == 'coordinator':
            return True


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow not safe methods to admin.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        elif request.user and request.user.is_superuser:
            return True


class IsAdminOrReadOnly(IsAdmin):
    """
    Custom permission to only allow not safe methods to admin.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return super(IsAdminOrReadOnly, self).has_permission(request, view)
