import pytest
from core.models import Lesson

@pytest.mark.django_db
def test_lesson(client):
    lesson = Lesson.objects.all()[0]
    response = client.get('/lesson/' + lesson.slug)
    assert response.status_code == 200
    assert lesson.name.encode('utf-8') in response.content
