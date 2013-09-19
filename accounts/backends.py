# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class TimtecModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, None)

        try:
            validate_email(username)
            field = 'email'
        except ValidationError:
            field = 'username'
        kwargs = {field: username}

        try:
            user = UserModel.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
