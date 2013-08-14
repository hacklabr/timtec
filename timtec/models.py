import re
import sqlalchemy as sa
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
)
from zope.sqlalchemy import ZopeTransactionExtension
from horus.models import (
    GroupMixin,
    UserMixin,
    UserGroupMixin,
    ActivationMixin,
)


class BaseModel(object):
    """Base class which auto-generates tablename, and surrogate
    primary key column.
    """
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    @declared_attr
    def id(self):
        return sa.Column(sa.Integer, primary_key=True)

    _traversal_lookup_key = 'id'

    @declared_attr
    def __tablename__(cls):
        """Convert CamelCase class name to underscores_between_words
        table name."""
        name = cls.__name__.replace('Mixin', '')

        return (
            name[0].lower() +
            re.sub(r'([A-Z])', lambda m: '_' + m.group(0).lower(), name[1:])
        )


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base(cls=BaseModel)


class User(UserMixin, Base):
    name = sa.Column(sa.Unicode(255))


class Group(GroupMixin, Base):
    pass


class UserGroup(UserGroupMixin, Base):
    pass


class Activation(ActivationMixin, Base):
    pass


class Badge(Base):
    name = sa.Column(sa.Unicode(255), nullable=False)
    users = relationship('UserBadge', backref='badges')


class UserBadge(Base):
    user_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)))
    badge_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Badge.__tablename__)))


class Video(Base):
    name = sa.Column(sa.Unicode(255))
    youtube_id = sa.Column(sa.Unicode(255))
    accesses = relationship('AccessedVideo', backref='access_videos')
    block = relationship('Block', uselist=False)

    def __json__(self, request):
        return {u'youtube_id': self.youtube_id, u'name': self.name}


class AccessedVideo(Base):
    video_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Video.__tablename__)))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)))
    start = sa.Column(sa.DateTime())
    stop = sa.Column(sa.DateTime())
    position = sa.Column(sa.Integer())


class Course(Base):
    """Course """
    slug = sa.Column(sa.Unicode(255), nullable=False)
    name = sa.Column(sa.Unicode(255))
    description = sa.Column(sa.UnicodeText())
    abstract = sa.Column(sa.UnicodeText())
    knowledge_acquired = sa.Column(sa.UnicodeText())
    knowledge_required = sa.Column(sa.UnicodeText())
    professors = relationship('CourseProfessors', backref='course')
    intro_video_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Video.__tablename__)))
    intro_video = relationship('Video')
    students = relationship('CourseStudents', backref='courses')
    status = sa.Column(sa.Unicode(255))
    # discutir com anderson como vai ser o tempo estimado
    time_estimated = sa.Column(sa.Unicode(255))
    extra_dadication = sa.Column(sa.Unicode(255))
    publication_date = sa.Column(sa.Date())

    def __unicode__(self):
        """This is used to render the model in a relation field. Must return an
        unicode string."""
        return self.name

    def __repr__(self):
        return '<Curso {0}>'.format(self.name)
#     wiki
#     forum
#     notes


class CourseStudents(Base):
    course_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Course.__tablename__)))
    students_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)))
    enrollment = sa.Column(sa.DateTime())


class CourseProfessors(Base):
    course_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Course.__tablename__)), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)), nullable=False)
    user = relationship('User', backref='course')
    start = sa.Column(sa.DateTime())
    biography = sa.Column(sa.UnicodeText())
    # couse role


class Lesson(Base):
    name = sa.Column(sa.Unicode(255))
    desc = sa.Column(sa.Unicode(255))
    position = sa.Column(sa.Integer())
    course_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Course.__tablename__)))
    course = relationship('Course', backref='lessons')
    students = relationship('LessonStudent', backref='lessons')
    blocks = relationship('Block', secondary='lesson_block', order_by="Block.position")


class LessonStudent(Base):
    lesson_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Lesson.__tablename__)))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)))
    start = sa.Column(sa.DateTime())
    end = sa.Column(sa.DateTime())
    progress = sa.Column(sa.Integer())


class Note(Base):
    text = sa.Column(sa.UnicodeText())
    video_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Video.__tablename__)))
    lesson_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Lesson.__tablename__)))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)))


class Access(Base):
    user_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)))


class Activity(Base):
    """Generic class to activities
    Data templates (data e type atributes):
    Multiple choice
        type: multiplechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choices: [0, 2, 5]} # list of espected choices, zero starting
    Single choice
        type: singlechoice
        data: {question: "", choices: ["choice1", "choice2", ...]}
        expected_answer_data: {choice: 1}
    """
    title = sa.Column(sa.Unicode(255))
    type = sa.Column(sa.Unicode(255))
    data = sa.Column(sa.UnicodeText())
    expected_answer_data = sa.Column(sa.UnicodeText())
    block = relationship('Block', uselist=False)

    def __json__(self, request):
        return {
            u'title': self.title,
            u'type': self.type,
            u'data': self.data,
            u'expected_answer_data': self.expected_answer_data
        }


class Block(Base):
    activity_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Activity.__tablename__)))
    activity = relationship('Activity', uselist=False)
    video_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Video.__tablename__)))
    video = relationship('Video', uselist=False)
    lessons = relationship('Lesson', secondary='lesson_block')
    position = sa.Column(sa.Integer())

    def __json__(self, request):
            return {u'activity': self.activity, u'video': self.video, u'position': self.position}


lesson_block = sa.Table('lesson_block', Base.metadata,
                        sa.Column(u'lesson_id', sa.Integer, sa.ForeignKey('{0}.id'.format(Lesson.__tablename__))),
                        sa.Column(u'block_id', sa.Integer, sa.ForeignKey('{0}.id'.format(Block.__tablename__))),
                        )


class Answer(Base):
    activity_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(Activity.__tablename__)))
    activity = relationship('Activity', uselist=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('{0}.id'.format(User.__tablename__)), nullable=False)
    user = relationship('User', uselist=False)
    timestamp = sa.Column(sa.DateTime())
    free_text_answer = sa.Column(sa.UnicodeText())
