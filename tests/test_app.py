import transaction
from pkg_resources import resource_filename
from pyramid import (
    testing,
    router,
)
from timtec.models import DBSession

config = None


def setup():
    global config
    config = testing.setUp()
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    from timtec.models import (
        Base,
        User,
    )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = User(username='one', password='kdkdk', email='skdsk')
        DBSession.add(model)


def teardown():
    DBSession.remove()
    testing.tearDown()


def test_app_creation():
    from paste.deploy.loadwsgi import appconfig
    from timtec import main
    settings = appconfig('config:' + resource_filename(__name__, '../development.ini'))
    app = main(config, **settings)
    assert isinstance(app, router.Router)


def test_course():
    from timtec.models import Course
    course = Course(name='Nome', description='desc')
    assert course.name == 'Nome'
    assert course.description == 'desc'


def test_course_class():
    from timtec.models import Lesson
    course_class = Lesson(name='Nome')
    assert course_class.name == 'Nome'


def test_video():
    from timtec.models import Video
    video = Video(name='Nome')
    assert video.name == 'Nome'
