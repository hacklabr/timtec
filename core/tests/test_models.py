# coding: utf-8

import pytest

from model_mommy import mommy
from core.models import CourseStudent


@pytest.mark.django_db
def test_percent_progress_by_lesson(user):
    from datetime import datetime
    course = mommy.make('Course')
    lesson = mommy.make('Lesson', name='Test Course', slug='test-lesson', status='published', course=course)
    mommy.make('Lesson', name='Test Course', slug='test-lesson-draft', status='draft', course=course)
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
    assert progress[0]['name'] == lesson.name
    assert progress[0]['slug'] == lesson.slug
    assert progress[0]['progress'] == 75

    # Ensure lesson-draft is not in result
    assert len(progress) == 1


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

    lesson1 = mommy.make('Lesson', slug='lesson1', desc='', name='l1',
                         notes='', course=course, position=1, status='published')
    lesson2 = mommy.make('Lesson', slug='lesson2', desc='', name='l1',
                         notes='', course=course, position=2, status='published')
    lesson3 = mommy.make('Lesson', slug='lesson3', desc='', name='l12341',
                         notes='', course=course, position=3, status='draft')
    assert course_student.resume_next_unit() is None

    unit1 = mommy.make('Unit', title='unit1', lesson=lesson1)
    assert course_student.resume_next_unit() == unit1

    unit2 = mommy.make('Unit', title='unit2', lesson=lesson1)
    assert course_student.resume_next_unit() == unit1

    unit3 = mommy.make('Unit', title='unit2', lesson=lesson2)
    assert course_student.resume_next_unit() == unit1

    # Draft lesson
    mommy.make('Unit', title='unit2', lesson=lesson3)
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


@pytest.mark.django_db
def test_min_percent_range():
    course = mommy.make('Course')

    assert course.min_percent_to_complete <= 100


@pytest.mark.django_db
def test_course_serializer():
    from core.serializers import CourseSerializer
    course = mommy.make('Course')

    course_serializer = CourseSerializer(course)

    assert course.min_percent_to_complete == \
        course_serializer.field_mapping.get("min_percent_to_complete",
                                            100)


@pytest.mark.django_db
def test_studentprogress_emmit_receipt(user):
    from datetime import datetime

    course = mommy.make('Course')
    classe = mommy.make('Class', course=course, students=[user])
    course_student = mommy.make('CourseStudent', user=user, course=course)
    assert course_student.reached_last_unit() is False

    lesson1 = mommy.make('Lesson', slug='lesson1', desc='', name='l1',
                         notes='', course=course, position=1, status='published')
    lesson2 = mommy.make('Lesson', slug='lesson2', desc='', name='l1',
                         notes='', course=course, position=2, status='published')
    mommy.make('Lesson', slug='lesson3', desc='', name='l1', notes='',
               course=course, position=3, status='published')
    mommy.make('Lesson', slug='lesson4', desc='', name='l1', notes='',
               course=course, position=4, status='draft')
    assert course_student.reached_last_unit() is False

    unit1 = mommy.make('Unit', title='unit1', lesson=lesson1)
    unit2 = mommy.make('Unit', title='unit2', lesson=lesson1)
    unit3 = mommy.make('Unit', title='unit3', lesson=lesson2)
    assert course_student.resume_next_unit() == unit1
    assert course_student.reached_last_unit() is False

    mommy.make('StudentProgress', user=user, unit=unit1,
               complete=datetime.now())

    mommy.make('StudentProgress', user=user, unit=unit2,
               complete=datetime.now())
    assert course_student.resume_next_unit() == unit3
    assert course_student.reached_last_unit() is False
    assert course_student.course_finished is False
    assert course_student.can_emmit_receipt() is False

    mommy.make('StudentProgress', user=user, unit=unit3,
               complete=datetime.now())
    assert course_student.resume_next_unit() == unit1
    assert course_student.reached_last_unit() is True
    assert course_student.course_finished is True
    assert course_student.can_emmit_receipt() is False
    # here, can't emmit because the course is complete but the class can not certificate

    classe.user_can_certificate = True
    classe.save()
    assert course_student.can_emmit_receipt() is True

    user.last_name = "Cool Lastname"
    user.save()
    unit4 = mommy.make('Unit', title='unit4', lesson=lesson2)
    mommy.make('StudentProgress', user=user, unit=unit4,
               complete=datetime.now())

    assert course_student.resume_next_unit() == unit1
    assert course_student.reached_last_unit() is True
    assert course_student.course_finished is True
    assert course_student.can_emmit_receipt() is True

    try:
        mommy.make('CourseCertification',
                   course_student=course_student)
    except Exception as e:
        assert type(e).__name__ == "IntegrityError"
