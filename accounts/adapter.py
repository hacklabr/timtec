from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from accounts.models import TimtecUser


class TimtecAdapter(DefaultAccountAdapter):
    def clean_username(self, username):
        USERNAME_REGEX = TimtecUser.USERNAME_REGEXP
        if not USERNAME_REGEX.match(username):
            raise ValidationError(_("Usernames can only contain "
                                    "letters, digits and ./-/_."))
        return super(TimtecAdapter, self).clean_username(username)
