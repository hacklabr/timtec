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
    unit1 = mommy.make('Unit', lesson=lesson, video=video)
    mommy.make('Activity', unit=unit1)
    unit2 = mommy.make('Unit', lesson=lesson, video=None)
    mommy.make('Activity', unit=unit2)
    unit3 = mommy.make('Unit', lesson=lesson, video=video)
    unit4 = mommy.make('Unit', lesson=lesson, video=video)
    course_student = mommy.make('CourseStudent', course=course, user=user)
    mommy.make('StudentProgress', user=user, unit=unit1, complete=datetime.now())
    mommy.make('StudentProgress', user=user, unit=unit2, complete=datetime.now())
    mommy.make('StudentProgress', user=user, unit=unit3, complete=datetime.now())
    mommy.make('StudentProgress', user=user, unit=unit4)

    progress = course_student.percent_progress_by_lesson()
    assert progress[0]['name'] == 'Test Course'
    assert progress[0]['slug'] == 'test-course'
    assert progress[0]['progress'] == 75


@pytest.mark.django_db
def test_lesson_counts(settings):
    lesson = mommy.make('Lesson', slug='lesson')
    video = mommy.make('Video')
    unit1 = mommy.make('Unit', lesson=lesson, video=video)
    unit2 = mommy.make('Unit', lesson=lesson, video=None)
    unit3 = mommy.make('Unit', lesson=lesson, video=video)
    mommy.make('Unit', lesson=lesson, video=video)
    mommy.make('Activity', unit=unit1)
    mommy.make('Activity', unit=unit1)
    mommy.make('Activity', unit=unit2)
    mommy.make('Activity', unit=unit3)

    assert lesson.activity_count() == 4
    assert lesson.video_count() == 3
    assert lesson.unit_count() == 4


@pytest.mark.django_db
def test_position_counter_for_new_units():
    lesson = mommy.make('Lesson', slug='lesson')

    assert mommy.make('Unit', lesson=lesson).position == 0
    assert mommy.make('Unit', lesson=lesson).position == 1
    assert mommy.make('Unit', lesson=lesson).position == 2


@pytest.mark.django_db
def test_enroll_user_create_single_entry_of_coursestudent(user):
    course = mommy.make('Course', slug='dbsql1234')

    assert CourseStudent.objects.filter(user=user, course=course).count() == 0

    course.enroll_student(user)
    assert CourseStudent.objects.filter(user=user, course=course).count() == 1


@pytest.mark.django_db
def test_resume(user):
    from datetime import datetime

    course = mommy.make('Course')
    course_student = mommy.make('CourseStudent', user=user, course=course)
    assert course_student.resume_next_unit() is None

    lesson1 = mommy.make('Lesson', slug='lesson1', desc='', name='l1', notes='', course=course, position=1)
    lesson2 = mommy.make('Lesson', slug='lesson2', desc='', name='l1', notes='', course=course, position=2)
    mommy.make('Lesson', slug='lesson3', desc='', name='l1', notes='', course=course, position=3)
    assert course_student.resume_next_unit() is None

    unit1 = mommy.make('Unit', title='unit1', lesson=lesson1)
    assert course_student.resume_next_unit() == unit1

    unit2 = mommy.make('Unit', title='unit2', lesson=lesson1)
    assert course_student.resume_next_unit() == unit1

    unit3 = mommy.make('Unit', title='unit2', lesson=lesson2)
    assert course_student.resume_next_unit() == unit1

    mommy.make('StudentProgress', user=user, unit=unit1, complete=datetime.now())
    assert course_student.resume_next_unit() == unit2

    mommy.make('StudentProgress', user=user, unit=unit2, complete=datetime.now())
    assert course_student.resume_next_unit() == unit3

    mommy.make('StudentProgress', user=user, unit=unit3, complete=datetime.now())
    assert course_student.resume_next_unit() == unit1


@pytest.mark.django_db
def test_get_current_user_classes(user):
    course = mommy.make('Course')
    course_professor = mommy.make('CourseProfessor', user=user, course=course)
    klass = mommy.make('Class', assistant=user, course=course)

    assert klass == course_professor.get_current_user_classes()[0]
