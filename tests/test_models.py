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


class TestVideo(BaseTestCase):
    def test(self):
        from timtec.models import Video
        video = Video(name='Video de teste', youtube_id='http://timtec.com.br')
        self.session.add(video)
        #transaction.commit()
        query = self.session.query(Video.name).filter_by(name='Video de teste')
        name = query.all()[0][0]
        assert video.name == name
