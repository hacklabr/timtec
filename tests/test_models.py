import pytest
from course.models import *


@pytest.mark.django_db
def test_super_user():
    a = TimtecUser.objects.get(username='a')
    assert a.is_superuser
