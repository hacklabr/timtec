from django.contrib.auth import get_user_model

import pytest
from model_mommy import mommy

User = get_user_model()


@pytest.mark.django_db
def test_lesson(admin_client):
    lesson = mommy.make('Lesson', slug='lesson', status='published')
    response = admin_client.get('/course/' + lesson.course.slug + '/lesson/' + lesson.slug + '/')
    assert response.status_code == 200
    assert lesson.name.encode('utf-8') in response.content


def create_professor(course, professor_user_name, professor_email, role):
    professor = User.objects.create_user(professor_user_name, professor_email, 'password')

    mommy.make('CourseProfessor', user=professor, course=course)

    non_coordinator_course_professor = course.courseprofessor_set.filter(user=professor)
    non_coordinator_course_professor.role = role

    return professor


@pytest.mark.django_db
def test_assistant_professor_should_cannot_change_class_professor(client):

    course = mommy.make('Course', slug='dbsql', name='Test course name')

    coordinator_professor = create_professor(course, 'coordinator_professor', 'coordinator_professor@test.com', 'coordinator')

    assistant_professor = create_professor(course, 'assistant_professor', 'assistant_professor@test.com', 'assistant')

    another_assistant = create_professor(course, 'another_assistant', 'another_assistant@test.com', 'assistant')

    clazz = mommy.make('Class', name='Test class name', course=course, assistant=coordinator_professor)

    client.login(username=assistant_professor.username, password='password')

    # post passing new_assistant as new assistant
    response = client.post('/class/' + str(clazz.id) + '/', {'assistant': another_assistant})
    assert response.status_code == 403


@pytest.mark.django_db
def test_coordinator_professor_should_can_change_class_professor(client):

    course = mommy.make('Course', slug='dbsql', name='Test course name')

    coordinator_professor = create_professor(course, 'coordinator_professor', 'coordinator_professor@test.com', 'coordinator')

    assistant_professor = create_professor(course, 'assistant_professor', 'assistant_professor@test.com', 'assistant')

    another_assistant = create_professor(course, 'another_assistant', 'another_assistant@test.com', 'assistant')

    clazz = mommy.make('Class', name='Test class name', course=course, assistant=assistant_professor)

    client.login(username=coordinator_professor.username, password='password')

    # post passing new_assistant as new assistant
    response = client.post('/class/' + str(clazz.id) + '/', {'assistant': another_assistant})
    assert response.status_code == 403
