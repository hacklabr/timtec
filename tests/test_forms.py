import pytest

from django.contrib.auth import get_user_model
from accounts.forms import ProfileEditForm

@pytest.mark.django_db
def test_profile_edit_forms_works_with_valid_data():
    user = get_user_model().objects.get(username='abcd')

    assert user.email == 'a@b.cd'

    data = {
        'username': 'abcd',
        'email': 'email@changed.com',
        'password1': '123456',
        'password2': '123456',
    }

    form = ProfileEditForm(instance=user, data=data)
    assert form.is_valid() is True, form.errors
    form.save()

    user = get_user_model().objects.get(username='abcd')
    assert user.email == 'email@changed.com'

@pytest.mark.django_db
def test_form_becomes_invalid_with_differents_passwords():
    user = get_user_model().objects.get(username='abcd')

    data = {
        'username': 'abcd',
        'email': 'a@b.cd',
        'password1': 'password_one',
        'password2': 'password_two',
    }

    form = ProfileEditForm(instance=user, data=data)
    assert form.is_valid() is False, form.errors
    assert 'password2' in form.errors