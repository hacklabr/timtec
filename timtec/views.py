from pyramid.view import view_config, view_defaults
from .models import (
    DBSession,
    Course,
    Lesson,
)


class BaseView(object):
    def __init__(self, request):
        self.request = request


class CourseController(BaseView):
    @view_config(route_name='index', renderer='templates/course_intro.pt')
    @view_config(route_name='course_intro', renderer='templates/course_intro.pt')
    def intro(self):
        course_slug = self.request.matchdict.get('course', 'dbsql')
        course = DBSession.query(Course).filter(Course.slug == course_slug).first()
        first_lesson = DBSession.query(Lesson).filter(Course.slug == course_slug) \
            .join(Course.lessons).filter(Lesson.position == 1).first()
        if first_lesson:
            first_lesson_url = self.request.route_path('lesson', course=course_slug, lesson=first_lesson.name)
        else:
            first_lesson_url = ''
        return {u'course': course, u'first_lesson_url': first_lesson_url}

    @view_config(route_name='lesson', renderer='templates/lesson.pt')
    def lesson(self, course_slug=u'dbsql'):
        course_slug = self.request.matchdict['course']
        lesson_name = self.request.matchdict['lesson']
        lesson = DBSession.query(Lesson).join(Lesson.course) \
            .filter(Lesson.name == lesson_name).filter(Course.slug == course_slug).first()
        return {u'lesson': lesson}


@view_defaults(route_name='lesson_rest', renderer="json")
class LessonRest(BaseView):
    @view_config(request_method='GET')
    def get(self):
        course_slug = self.request.matchdict['course']
        lesson_name = self.request.matchdict['lesson']
        lesson = DBSession.query(Lesson).join(Lesson.course) \
            .filter(Lesson.name == lesson_name).filter(Course.slug == course_slug).first()
        return {u'blocks': lesson.blocks}


class UserController(BaseView):
    @view_config(route_name='profile', renderer='templates/profile.pt')
    def profile(self):
        return {}

    @view_config(route_name='edit_profile', renderer='templates/edit_profile.pt')
    def profile_edit(self):
        return {}

    @view_config(route_name='user_notes', renderer='templates/user_notes.pt')
    def user_notes(self):
        return {}

    @view_config(route_name='user_note', renderer='templates/user_note.pt')
    def user_note(self):
        return {}

    @view_config(route_name='user_courses', renderer='templates/user_courses.pt')
    def user_courses(self):
        return {}


class ForumController(BaseView):
    @view_config(route_name='course_forum', renderer='templates/course_forum.pt')
    def course_forum(self):
        return {}

    @view_config(route_name='question', renderer='templates/question.pt')
    def question(self):
        return {}
