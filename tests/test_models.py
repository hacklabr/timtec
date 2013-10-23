import pytest

from os.path import join, dirname
from model_mommy import mommy
from django.core.files.base import ContentFile
from core.models import TimtecUser, Course, CourseStudent


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
def test_position_counter_for_new_units():
    lesson = mommy.make('Lesson')

    assert mommy.make('Unit', lesson=lesson).position == 0
    assert mommy.make('Unit', lesson=lesson).position == 1
    assert mommy.make('Unit', lesson=lesson).position == 2


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


@pytest.mark.django_db
def test_enroll_user_create_single_entry_of_coursestudent():
    user = TimtecUser.objects.get(username='abcd')
    course = Course.objects.get(slug='dbsql')

    assert CourseStudent.objects.filter(user=user, course=course).count() == 0

    course.enroll_student(user)
    assert CourseStudent.objects.filter(user=user, course=course).count() == 1

    course.enroll_student(user)
    assert CourseStudent.objects.filter(user=user, course=course).count() == 1
