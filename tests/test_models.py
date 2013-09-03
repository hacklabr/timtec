import pytest

from os.path import join, dirname
from model_mommy import mommy
from django.core.files.base import ContentFile
from core.models import *


@pytest.mark.django_db
def test_super_user():
    a = TimtecUser.objects.get(username='abcd')
    assert a.is_superuser


@pytest.mark.django_db
def test_lesson_counts(settings):
    lesson = mommy.make('Lesson')
    video = mommy.make('Video')
    activity = mommy.make('Activity')
    mommy.make('Unit', lesson=lesson, video=video, activity=activity)
    mommy.make('Unit', lesson=lesson, video=None, activity=activity)
    mommy.make('Unit', lesson=lesson, video=video, activity=None)
    mommy.make('Unit', lesson=lesson, video=video, activity=None)

    assert lesson.activity_count() == 2
    assert lesson.video_count() == 3
    assert lesson.unit_count() == 4


@pytest.mark.django_db
def test_user_picture_url():
    user = TimtecUser.objects.get(username='abcd')

    assert not user.picture
    assert user.get_picture_url() == '/static/img/avatar-default.png'

    testpicture = join(dirname(__file__), 'testdata', 'nobody.png')
    user.picture.save('abcd-avatar.png', ContentFile(open(testpicture).read()))
    user.save()

    user = TimtecUser.objects.get(username='abcd')
    assert user.get_picture_url() == '/media/user-pictures/abcd-avatar.png'

    #teardown
    user.picture.delete()