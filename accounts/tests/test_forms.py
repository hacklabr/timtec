import pytest
from accounts.forms import ProfileEditForm


@pytest.mark.django_db
def test_profile_edit_forms_works_with_valid_data(user):
    data = {
        'username': user.username,
        'email': 'email@changed.com',
        'password1': '123456',
        'password2': '123456',
    }

    form = ProfileEditForm(instance=user, data=data)
    assert form.is_valid() is True, form.errors
    form.save()

    assert user.email == 'email@changed.com'


@pytest.mark.django_db
def test_form_becomes_invalid_with_different_passwords(user):
    data = {
        'username': user.username,
        'email': user.email,
        'password1': 'password_one',
        'password2': 'password_two',
    }

    form = ProfileEditForm(instance=user, data=data)
    assert form.is_valid() is False, form.errors
    assert 'password2' in form.errors
