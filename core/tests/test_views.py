import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_lesson(admin_client):
    lesson = mommy.make('Lesson')
    response = admin_client.get('/course/' + lesson.course.slug + '/lesson/' + lesson.slug + '/')
    assert response.status_code == 200
    assert lesson.name.encode('utf-8') in response.content
