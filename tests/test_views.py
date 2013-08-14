# coding: utf-8

from pyramid import testing
from paste.deploy.loadwsgi import appconfig
import mock
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from timtec.models import (
    Base,
)
import os
here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../', 'test.ini'))

engine = None
Session = None


def setup_module(module):
    global engine, Session
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)


class BaseTestCase():
    def setup_method(self, method):
        testing.setUp()
        self.session = Session(bind=engine)
        Base.session = self.session
        self.patcher = mock.patch('timtec.views.DBSession', self.session)
        self.patcher.start()

    def teardown_method(self, method):
        self.session.rollback()
        try:
            self.patcher.stop()
        except:
            pass
        testing.tearDown()


class TestViews(BaseTestCase):
    def test_course_intro(self):
        from timtec.views import CourseController
        from timtec.models import (
            Course,
            CourseProfessors,
            User,
        )
        course = Course()
        course.slug = u'dbsql'
        course.name = u'Banco de Dados e SQL'
        course.description = u'Introdução a Bancos de Dados e Linguagem SQL'

        user = User(username='ramalho', password='kdkdk', email='skdsk@vcx')
        user.name = u'Luciano Ramalho'
        course_professors = CourseProfessors()
        course_professors.user = user
        course_professors.biography = (
            u'Mussum ipsum cacilds, vidis litro abertis. Consetis'
            u'adipiscings elitis. Pra lá , depois divoltis porris,'
            u'paradis. Paisis, filhis, espiritis santis. Mé faiz elementum'
            u' girarzis, nisi eros vermeio, in elementis mé pra quem é'
            u'amistosis quis leo. Manduma pindureta quium dia nois paga.'
            u'bolis eu num gostis.'
        )
        course.professors.append(course_professors)
        self.session.add(course)

        request = testing.DummyRequest()
        request.matchdict['course'] = u'dbsql'
        course_controller = CourseController(request)
        response = course_controller.intro()
        assert response['course'] == course
        assert response['course'].professors[0] == course_professors
        assert response['course'].professors[0].user == user

    def test_lesson(self):
        from timtec.views import CourseController
        from timtec.models import (
            Course,
            CourseProfessors,
            User,
            Lesson,
            Video,
            Block,
            Activity,
        )
        course = Course()
        course.slug = u'dbsql'
        course.name = u'Banco de Dados e SQL'
        course.description = u'Introdução a Bancos de Dados e Linguagem SQL'

        user = User(username='ramalho', password='kdkdk', email='skdsk@vcx')
        user.name = u'Luciano Ramalho'
        course_professors = CourseProfessors()
        course_professors.user = user
        course_professors.biography = (
            u'Mussum ipsum cacilds, vidis litro abertis. Consetis'
            u'adipiscings elitis. Pra lá , depois divoltis porris,'
            u'paradis. Paisis, filhis, espiritis santis. Mé faiz elementum'
            u' girarzis, nisi eros vermeio, in elementis mé pra quem é'
            u'amistosis quis leo. Manduma pindureta quium dia nois paga.'
            u'bolis eu num gostis.'
        )
        course.professors.append(course_professors)
        self.session.add(course)

        lesson = Lesson()
        lesson.name = u'Apresentando: Bancos de Dados'
        lesson.desc = u'Para que servem os bancos de dados'
        course.lessons.append(lesson)
        self.session.add(lesson)

        # Create blocks
        activity1 = Activity()
        activity1.title = u'Exercício multipla escolha1'
        self.session.add(activity1)

        video1 = Video()
        video1.name = u'Video 1 de teste'
        self.session.add(video1)

        block1 = Block()
        block1.activity = activity1
        block1.video = video1
        block1.lessons.append(lesson)
        self.session.add(block1)

        request = testing.DummyRequest()
        request.matchdict['course'] = u'dbsql'
        request.matchdict['lesson'] = u'Apresentando: Bancos de Dados'
        course_controller = CourseController(request)
        response = course_controller.lesson()

        assert response['lesson'] == lesson
        assert response['lesson'].course == course
        assert response['lesson'].blocks[0] == block1
        assert response['lesson'].blocks[0].video == video1

    def test_index(self):
        from timtec.views import CourseController
        from timtec.models import (
            Course,
        )

        course = Course()
        course.slug = u'dbsql'
        self.session.add(course)

        request = testing.DummyRequest()
        course_controller = CourseController(request)
        response = course_controller.intro()

        assert response['course'] == course

    def lesson_rest__get(self):
        from timtec.views import CourseController
        from timtec.models import (
            Course,
            CourseProfessors,
            User,
            Lesson,
            Video,
            Block,
            Activity,
        )
        import json
        course = Course()
        course.slug = u'dbsql'
        course.name = u'Banco de Dados e SQL'
        course.description = u'Introdução a Bancos de Dados e Linguagem SQL'

        user = User(username='ramalho', password='kdkdk', email='skdsk@vcx')
        user.name = u'Luciano Ramalho'
        course_professors = CourseProfessors()
        course_professors.user = user
        course_professors.biography = (
            u'Mussum ipsum cacilds, vidis litro abertis. Consetis'
            u'adipiscings elitis. Pra lá , depois divoltis porris,'
            u'paradis. Paisis, filhis, espiritis santis. Mé faiz elementum'
            u' girarzis, nisi eros vermeio, in elementis mé pra quem é'
            u'amistosis quis leo. Manduma pindureta quium dia nois paga.'
            u'bolis eu num gostis.'
        )
        course.professors.append(course_professors)
        self.session.add(course)

        lesson = Lesson()
        lesson.name = u'Apresentando: Bancos de Dados'
        lesson.desc = u'Para que servem os bancos de dados'
        course.lessons.append(lesson)
        self.session.add(lesson)

        # Create blocks
        activity1 = Activity()
        activity1.title = u'Exercício multipla escolha1'
        self.session.add(activity1)

        video1 = Video()
        video1.name = u'Video 1 de teste'
        self.session.add(video1)

        block1 = Block()
        block1.activity = activity1
        block1.video = video1
        block1.lessons.append(lesson)
        self.session.add(block1)

        request = testing.DummyRequest()
        request.matchdict['course'] = u'dbsql'
        request.matchdict['lesson'] = u'Apresentando: Bancos de Dados'
        course_controller = CourseController(request)
        response = course_controller.lesson()

        response_dict = json.loads(response)

        assert response_dict['video']['name'] == u'Video 1 de teste'
        assert response_dict['activity']['title'] == u'Exercício multipla escolha1'
