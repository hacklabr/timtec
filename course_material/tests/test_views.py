import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_course_material(admin_client, user):
    course = mommy.make('Course', name='Test Course', slug='dbsql')
    mommy.make('Lesson', course=course)
    course_material = mommy.make('CourseMaterial', course=course, text='foobar**bold**')

    response = admin_client.get('/course_material/' + course.slug + '/')

    assert response.status_code == 200
    assert course_material.text[:6].encode('utf-8') in response.content
    # Test Markdown rendering
    assert '<strong>bold</strong>'.encode('utf-8') in response.content


@pytest.mark.django_db
def test_file_upload(rf, user):
    from course_material.views import FileUploadView
    import os

    file_name = 'media/dbsql/dummy_file.txt'
    if os.path.exists(file_name):
        os.remove(file_name)

    course = mommy.make('Course', name='Test Course', slug='dbsql')
    course_material = mommy.make('CourseMaterial', course=course, text='foobar**bold**')

    with open('course_material/tests/dummy_file.txt') as fp:
        request = rf.post('/course_material/file_upload/dbsql', {'file': fp})
        request.user = user
        view = FileUploadView(request=request)
        view.kwargs = {'slug': 'dbsql'}
        response = view.post(request)

    assert response.status_code == 200
    assert os.path.exists(file_name)
    assert course_material.files.all()[0].file.name == 'dbsql/dummy_file.txt'
    if os.path.exists(file_name):
        os.remove(file_name)
