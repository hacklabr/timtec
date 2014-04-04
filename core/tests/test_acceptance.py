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
    # assert response.status_code == 301
    assert response.status_code == 200


@pytest.mark.django_db
def test_enroll_user(client, user):
    course = mommy.make('Course', slug='acceptance_enroll_user')
    lesson = mommy.make('Lesson', course=course, slug='lesson')
    from core.models import CourseStudent

    assert not CourseStudent.objects.filter(user__username=user.username, course__slug=course.slug).exists()

    reponse = client.post('/login/', {'username': user.username, 'password': 'password'})
    reponse = client.get('/course/' + course.slug + '/enroll/')
    assert reponse['Location'] == 'http://testserver/course/' + course.slug + '/lesson/' + lesson.slug + '/'

    assert CourseStudent.objects.filter(user__username=user.username, course__slug=course.slug).exists()


@pytest.mark.django_db
def test_timtec_adapter_validates_username(client):
    mommy.make('Group', name="students")
    response = client.post('/accounts/signup/', {'username': "test", 'email': "test@example.com",
                                                 'password1': 123123, 'password2': 123123, "accept_terms": True})
    assert response.status_code == 302  # ok
    # assert "./-/_" not in response.content  # validator

    response = client.post('/accounts/signup/', {'username': "test@test", 'email': "test2@example.com",
                                                 'password1': 123123, 'password2': 123123, "accept_terms": True})
    assert response.status_code == 200  # ok
    # assert "./-/_" in response.content  # validator
