import pytest
from accounts.backends import TimtecModelBackend


@pytest.mark.django_db
def test_authenticate_with_email(user):
    backend = TimtecModelBackend()
    luser = backend.authenticate(username=user.email, password='password')
    assert luser.username == user.username


@pytest.mark.django_db
def test_authenticate_with_username(user):
    backend = TimtecModelBackend()
    luser = backend.authenticate(username=user.username, password='password')
    assert luser.username == user.username


@pytest.mark.django_db
def test_authenticate_with_email_field_explicitly(user):
    from django.contrib.auth import get_user_model
    Model = get_user_model()
    original_field = Model.USERNAME_FIELD

    Model.USERNAME_FIELD = 'email'
    backend = TimtecModelBackend()
    luser = backend.authenticate(email=user.email, password='password')
    assert luser.username == user.username

    Model.USERNAME_FIELD = original_field


@pytest.mark.django_db
def test_fail_with_invalid_email_or_username():
    backend = TimtecModelBackend()
    assert backend.authenticate(username='ivalid@email.com', password='x') is None
    assert backend.authenticate(username='invalid_username', password='x') is None
