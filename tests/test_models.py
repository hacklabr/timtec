# coding: utf-8

import pytest

from model_mommy import mommy
from django.core.files.base import ContentFile
from core.models import CourseStudent


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
def test_get_user_type(user):
    assert user.get_user_type() == "unidentified"


@pytest.mark.django_db
def test_username_validator():
    from core.models import TimtecUser
    from django.core.exceptions import ValidationError
    try:
        t = TimtecUser.objects.create(username="test@test", email="test@example.com")
        t.full_clean()
    except ValidationError:
        pass
    else:
        assert False


@pytest.mark.django_db
def test_user_picture_url():
    user = mommy.make('TimtecUser')
    user.username = u'Usér'
    user.save()

    assert not user.picture
    assert user.get_picture_url() == '/static/img/avatar-default.png'

    user.picture.save(u'abcd-ávatár.png', ContentFile('XXX'))
    user.username
    user.save()

    # file is saved as md5(filename + username)
    assert user.get_picture_url().startswith('/media/user-pictures/de7f72f1443cd5e3b63131ffbac0b83f')

    #teardown
    user.picture.delete()


@pytest.mark.django_db
def test_enroll_user_create_single_entry_of_coursestudent(user):
    course = mommy.make('Course', slug='dbsql1234')

    assert CourseStudent.objects.filter(user=user, course=course).count() == 0

    course.enroll_student(user)
    assert CourseStudent.objects.filter(user=user, course=course).count() == 1

    course.enroll_student(user)
    assert CourseStudent.objects.filter(user=user, course=course).count() == 1


@pytest.mark.django_db
def test_resume(user):
    from datetime import datetime

    course = mommy.make('Course')
    course_student = mommy.make('CourseStudent', user=user, course=course)
    assert course_student.resume_course() is None

    lesson = mommy.make('Lesson', desc='', name='l1', notes='', course=course)
    assert course_student.resume_course() is None

    unit1 = mommy.make('Unit', title='unit1', lesson=lesson)
    assert course_student.resume_course() == unit1

    unit2 = mommy.make('Unit', title='unit2', lesson=lesson)
    assert course_student.resume_course() == unit1

    mommy.make('StudentProgress', user=user, unit=unit2, complete=datetime.now())
    assert course_student.resume_course() == unit2

    mommy.make('StudentProgress', user=user, unit=unit1, complete=datetime.now())
    assert course_student.resume_course() == unit1
