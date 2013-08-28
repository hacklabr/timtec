import pytest
from core.models import Lesson


@pytest.mark.django_db
def test_lesson(admin_client):
    lesson = Lesson.objects.all()[0]
    response = admin_client.get('/lesson/' + lesson.slug)
    assert response.status_code == 200
    assert lesson.name.encode('utf-8') in response.content
