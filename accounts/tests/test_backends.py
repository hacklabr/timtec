import pytest

from accounts.backends import TimtecModelBackend


@pytest.mark.django_db
def test_authenticate_with_email():
    backend = TimtecModelBackend()
    user = backend.authenticate(username='a@b.cd', password='x')
    assert user.username == 'abcd'


@pytest.mark.django_db
def test_authenticate_with_username():
    backend = TimtecModelBackend()
    user = backend.authenticate(username='abcd', password='x')
    assert user.email == 'a@b.cd'


@pytest.mark.django_db
def test_authenticate_with_email_field_explicitly():
    from django.contrib.auth import get_user_model
    Model = get_user_model()
    original_field = Model.USERNAME_FIELD

    Model.USERNAME_FIELD = 'email'
    backend = TimtecModelBackend()
    user = backend.authenticate(email='a@b.cd', password='x')
    assert user.username == 'abcd'

    Model.USERNAME_FIELD = original_field


@pytest.mark.django_db
def test_fail_with_invalid_email_or_username():
    backend = TimtecModelBackend()
    assert backend.authenticate(username='ivalid@email.com', password='x') is None
    assert backend.authenticate(username='invalid_username', password='x') is None
