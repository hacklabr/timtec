import pytest


@pytest.mark.django_db
def test_course_create_view(admin_client, client, user):
    from django.core.urlresolvers import reverse_lazy
    from core.models import Course
    response = admin_client.get(reverse_lazy('administration.new_course'))
    assert response.status_code == 405

    name = 'Test course'
    slug = 'test-course'
    base_url = 'http://testserver/admin/courses/{}/'

    client.login(username=user.username, password='password')
    response = client.post(reverse_lazy('administration.new_course'), {'name': name})
    assert response.status_code == 403

    response = admin_client.post(reverse_lazy('administration.new_course'), {'name': name})
    assert response.status_code == 302
    assert Course.objects.filter(slug=slug).exists()
    course = Course.objects.get(slug=slug)
    assert response.url == base_url.format(str(course.id))

    response = admin_client.post(reverse_lazy('administration.new_course'), {'name': name})
    slug += '1'
    assert response.status_code == 302
    assert Course.objects.filter(slug=slug).exists()
    course = Course.objects.get(slug=slug)
    assert response.url == base_url.format(str(course.id))
