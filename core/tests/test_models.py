# coding: utf-8

import pytest

from model_mommy import mommy
from core.models import CourseStudent


@pytest.mark.django_db
def test_percent_progress_by_lesson(user):
    from datetime import datetime
    course = mommy.make('Course')
    lesson = mommy.make('Lesson', name='Test Course', slug='test-course', course=course)
    video = mommy.make('Video')
    activity = mommy.make('Activity')
    unit1 = mommy.make('Unit', lesson=lesson, video=video, activity=activity)
    unit2 = mommy.make('Unit', lesson=lesson, video=None, activity=activity)
    unit3 = mommy.make('Unit', lesson=lesson, video=video, activity=None)
    unit4 = mommy.make('Unit', lesson=lesson, video=video, activity=None)
    course_student = mommy.make('CourseStudent', course=course, user=user)
    mommy.make('StudentProgress', user=user, unit=unit1, complete=datetime.now())
    mommy.make('StudentProgress', user=user, unit=unit2, complete=datetime.now())
    mommy.make('StudentProgress', user=user, unit=unit3, complete=datetime.now())
    mommy.make('StudentProgress', user=user, unit=unit4)

    progress = course_student.percent_progress_by_lesson()
    assert progress[0]['name'] == 'Test Course'
    assert progress[0]['slug'] == 'test-course'
    assert progress[0]['progress'] == 0.75


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
    assert course_student.resume_last_unit() is None

    lesson = mommy.make('Lesson', desc='', name='l1', notes='', course=course)
    assert course_student.resume_last_unit() is None

    unit1 = mommy.make('Unit', title='unit1', lesson=lesson)
    assert course_student.resume_last_unit() == unit1

    unit2 = mommy.make('Unit', title='unit2', lesson=lesson)
    assert course_student.resume_last_unit() == unit1

    mommy.make('StudentProgress', user=user, unit=unit2, complete=datetime.now())
    assert course_student.resume_last_unit() == unit2

    mommy.make('StudentProgress', user=user, unit=unit1, complete=datetime.now())
    assert course_student.resume_last_unit() == unit1
