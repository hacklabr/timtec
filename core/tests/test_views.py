# -*- coding: utf-8 -*-
import pytest
from model_mommy import mommy

from conftest import create_user
from core.models import Class


@pytest.mark.django_db
def test_lesson(admin_client):
    lesson = mommy.make('Lesson', slug='lesson', status='published')
    response = admin_client.get('/course/' + lesson.course.slug + '/lesson/' + lesson.slug + '/')
    assert response.status_code == 200
    assert lesson.name.encode('utf-8') in response.content


def assign_professor_to_course(course, existing_professor=None, new_professor_username=None, role=None):
    """

    :param existing_professor: Existing object TimtecUser
    :param new_professor_user_name: Non-existing professor username, if not defined, it will be created
    :param course: The course to assign professor to
    :param role: Role to assign to professor
    :return: The created/existing professor
    """

    if existing_professor is not None:
        professor = existing_professor
    else:
        professor = create_user(new_professor_username)

    mommy.make('CourseProfessor', user=professor, course=course, role=role)

    return professor


@pytest.mark.django_db
def test_assistant_professor_should_cannot_change_class_professor(client):
    course = mommy.make('Course', slug='dbsql', name='Test course name')

    coordinator_professor = assign_professor_to_course(course, new_professor_username='coordinator_professor', role='coordinator')

    assistant_professor = assign_professor_to_course(course, new_professor_username='assistant_professor', role='assistant')

    another_assistant = assign_professor_to_course(course, new_professor_username='another_assistant', role='assistant')

    klass = mommy.make('Class', name='Test class name', course=course, assistant=coordinator_professor)

    client.login(username=assistant_professor.username, password='password')

    response = client.post('/class/' + str(klass.id) + '/', {'name': 'A class', 'assistant': another_assistant.id})

    assert response.status_code == 403


@pytest.mark.django_db
def test_coordinator_professor_should_can_change_class_professor(client):
    course = mommy.make('Course', slug='dbsql', name='Test course name')

    coordinator_professor = assign_professor_to_course(course, new_professor_username='coordinator_professor', role='coordinator')

    assistant_professor = assign_professor_to_course(course, new_professor_username='assistant_professor', role='assistant')

    another_assistant = assign_professor_to_course(course, new_professor_username='another_assistant', role='assistant')

    klass = mommy.make('Class', name='A class', course=course, assistant=assistant_professor)

    client.login(username=coordinator_professor.username, password='password')

    response = client.post('/class/' + str(klass.id) + '/', {'name': 'A class', 'assistant': another_assistant.id})

    # A página redireciona para outro lugar em caso de sucesso
    assert response.status_code == 302

    changed_class = Class.objects.get(id=klass.id)

    assert changed_class.assistant == another_assistant
