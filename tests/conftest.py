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


@pytest.fixture()
def admin_user(db):
    """A Django test client logged in as an admin user"""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        user = User.objects.create_user('admin', 'admin@example.com',
                                        'password')
        user.is_staff = True
        user.is_superuser = True
        user.save()
    return user


@pytest.fixture()
def user(db):
    """A Django test client logged in as an admin user"""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        User.objects.get(email='admin@example.com')
    except User.DoesNotExist:
        user = User.objects.create_user('abcd', 'admin@example.com',
                                        'x')
        user.save()
    return user
