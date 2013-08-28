import pytest


@pytest.mark.django_db
def test_is_admin_working(client):
    response = client.get('/admin/')
    assert response.status_code == 200
    assert 'Timtec Admin' in response.content


@pytest.mark.django_db
def test_mainview(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.has_header('Location')
    assert response['Location'] == 'http://testserver/course/dbsql'


def test_admin_user(admin_client):
    response = admin_client.get('/admin/core/timtecuser/?q=luciano')
    assert 'luciano@ramalho.org' in response.content
