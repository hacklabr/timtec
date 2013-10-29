import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_is_admin_working(client):
    response = client.get('/django/admin/')
    assert response.status_code == 200
    assert 'Timtec Admin' in response.content


@pytest.mark.django_db
def test_mainview(client):
    mommy.make('Course')
    response = client.get('/')
    assert response.status_code == 302
    assert response.has_header('Location')
    assert 'testserver/course' in response['Location']


def test_admin_user(admin_client):
    response = admin_client.get('/django/admin/core/timtecuser/?q=admin')
    assert 'admin' in response.content


@pytest.mark.django_db
def test_username_login(client, user):
    response = client.post('/login/', {'username': user.username, 'password': 'password'})
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'


@pytest.mark.django_db
def test_email_login(client, user):
    response = client.post('/login/', {'username': user.email, 'password': 'password'})
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'


@pytest.mark.django_db
def test_next_field_still_works(client, user):
    reponse = client.post('/login/', {'username': user.email, 'password': 'password', 'next': '/profile/edit'})
    assert reponse.status_code == 302
    assert reponse['Location'] == 'http://testserver/profile/edit'


@pytest.mark.django_db
def test_enroll_user(client, user):
    course = mommy.make('Course', slug='acceptance_enroll_user')
    lesson = mommy.make('Lesson', course=course)
    from core.models import CourseStudent

    assert not CourseStudent.objects.filter(user__username=user.username, course__slug=course.slug).exists()

    reponse = client.post('/login/', {'username': user.username, 'password': 'password'})
    reponse = client.get('/course/' + course.slug + '/enroll')
    assert reponse['Location'] == 'http://testserver/lesson/' + lesson.slug

    assert CourseStudent.objects.filter(user__username=user.username, course__slug=course.slug).exists()
