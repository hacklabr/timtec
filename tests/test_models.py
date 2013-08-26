import pytest
from core.models import *


@pytest.mark.django_db
def test_super_user():
    a = TimtecUser.objects.get(username='a@b.cd')
    assert a.is_superuser
