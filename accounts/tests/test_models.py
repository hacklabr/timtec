# coding: utf-8

import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_get_user_type(user):
    assert user.get_user_type() == "unidentified"


@pytest.mark.django_db
def test_username_validator():
    from django.contrib.auth import get_user_model
    from django.core.exceptions import ValidationError
    try:
        TimtecUser = get_user_model()
        t = TimtecUser.objects.create(username="test@test", email="test@example.com")
        t.full_clean()
    except ValidationError:
        pass
    else:
        assert False


@pytest.mark.django_db
def test_user_picture_url():
    from django.core.files.base import ContentFile
    from django.contrib.auth import get_user_model
    TimtecUser = get_user_model()
    user = mommy.make(TimtecUser)
    user.username = u'Usér'
    user.save()

    assert not user.picture
    assert user.get_picture_url() == '/static/img/avatar-default.png'

    user.picture.save(u'abcd-ávatár.png', ContentFile('XXX'))
    user.username
    user.save()

    # file is saved as md5(filename + username)
    assert user.get_picture_url().startswith('/media/user-pictures/de7f72f1443cd5e3b63131ffbac0b83f')

    # teardown
    user.picture.delete()


@pytest.mark.django_db
def test_user_profile_property():
    from django.contrib.auth import get_user_model
    TimtecUser = get_user_model()
    user = mommy.make(TimtecUser)

    assert not user.is_profile_filled

    user.last_name = u'Cool Lastname'
    user.save()

    assert user.is_profile_filled is True

