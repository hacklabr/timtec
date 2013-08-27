import pytest


@pytest.fixture()
def admin_client(db):
    """A Django test client logged in as an admin user"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    from django.test.client import Client

    try:
        User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        user = User.objects.create_user('admin', 'admin@example.com',
                                        'password')
        user.is_staff = True
        user.is_superuser = True
        user.save()

    client = Client()
    client.login(username='admin@example.com', password='password')
    return client


@pytest.mark.django_db
def test_is_admin_working(client):
    response = client.get('/admin/')
    assert response.status_code == 200
    assert 'Timtec Admin' in response.content


@pytest.mark.django_db
def test_mainview(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Timtec' in response.content


def test_admin_user(admin_client):
    response = admin_client.get('/admin/core/timtecuser/?q=luciano')
    assert 'luciano@ramalho.org' in response.content
