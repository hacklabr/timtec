from rest_framework import permissions


class EditQuestionPermission(permissions.BasePermission):
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
        elif request.user == obj.user:
            return True
        elif request.user.groups.filter(name="professors"):
            # FIXME remove this after implement tutor professor
            return True
        elif obj.course.professors.filter(user=request.user):
            course_professor = obj.course.professors.filter(user=request.user)
            if course_professor.role == 'coordinator':
                return True
            elif course_professor.role == 'assistant':
                try:
                    question_user_class = obj.user.classes.get(course=obj.course)
                    if question_user_class in request.user.professor_classes.all():
                        return True
                except:
                    return False

class EditAnswerPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user in obj.question.course.professors.all():
            return True
        elif request.user == obj.user:
            return True
        elif request.user.groups.filter(name="professors"):
            # FIXME remove this after implement tutor professor
            return True
        elif obj.question.course.professors.filter(user=request.user):
            course_professor = obj.question.course.professors.filter(user=request.user)
            if course_professor.role == 'coordinator':
                return True
            elif course_professor.role == 'assistant':
                try:
                    question_user_class = obj.user.classes.get(course=obj.question.course)
                    if question_user_class in request.user.professor_classes.all():
                        return True
                except:
                    return False
