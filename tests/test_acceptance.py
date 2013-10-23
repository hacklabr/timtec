import pytest


@pytest.mark.django_db
def test_is_admin_working(client):
    response = client.get('/django/admin/')
    assert response.status_code == 200
    assert 'Timtec Admin' in response.content


@pytest.mark.django_db
def test_mainview(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.has_header('Location')
    assert response['Location'] == 'http://testserver/course/dbsql'


def test_admin_user(admin_client):
    response = admin_client.get('/django/admin/core/timtecuser/?q=luciano')
    assert 'luciano@ramalho.org' in response.content


@pytest.mark.django_db
def test_username_login(client):
    reponse = client.post('/login/', {'username': 'abcd', 'password': 'x'})
    assert reponse.status_code == 302
    assert reponse['Location'] == 'http://testserver/'


@pytest.mark.django_db
def test_email_login(client):
    reponse = client.post('/login/', {'username': 'a@b.cd', 'password': 'x'})
    assert reponse.status_code == 302
    assert reponse['Location'] == 'http://testserver/'


@pytest.mark.django_db
def test_next_field_still_works(client):
    reponse = client.post('/login/', {'username': 'a@b.cd', 'password': 'x', 'next': '/profile/edit'})
    assert reponse.status_code == 302
    assert reponse['Location'] == 'http://testserver/profile/edit'


@pytest.mark.django_db
def test_enroll_user(client):
    from core.models import CourseStudent

    assert not CourseStudent.objects.filter(user__username='abcd', course__slug='dbsql').exists()

    reponse = client.post('/login/', {'username': 'a@b.cd', 'password': 'x'})
    reponse = client.get('/course/dbsql/enroll')
    assert reponse['Location'] == 'http://testserver/lesson/aula-1-modelos-de-dados-e-introducao-ao-modelo-relacional'

    assert CourseStudent.objects.filter(user__username='abcd', course__slug='dbsql').exists()
