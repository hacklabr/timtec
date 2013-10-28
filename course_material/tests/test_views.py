import pytest


@pytest.mark.django_db
def test_course_material(rf):
    from core.models import TimtecUser
    from course_material.views import CourseMaterialView
    from course_material.models import CourseMaterial

    course_material = CourseMaterial.objects.get(course__slug='dbsql')
    request = rf.get('/course_material/dbsql')
    request.user = TimtecUser.objects.get(username='abcd')

    view = CourseMaterialView(request=request)
    view.kwargs = {'slug': 'dbsql'}

    response = view.get(request)
    response.render()
    assert response.status_code == 200
    assert course_material.text[:30].encode('utf-8') in response.content
    # Test Markdown rendering
    assert '<strong>Negrito</strong>'.encode('utf-8') in response.content


# TODO: bruno martin
#
# @pytest.mark.django_db
# def test_file_upload(rf):
#     from core.models import TimtecUser
#     from course_material.views import FileUploadView
#     from course_material.models import CourseMaterial
#     import os
#
#     with open('course_material/tests/dummy_file.txt') as fp:
#         request = rf.post('/course_material/file_upload/dbsql', {'file': fp})
#         request.user = TimtecUser.objects.get(username='abcd')
#         view = FileUploadView(request=request)
#         view.kwargs = {'slug': 'dbsql'}
#         response = view.post(request)
#
#     course_material = CourseMaterial.objects.get(course__slug='dbsql')
#     assert response.status_code == 200
#     assert os.path.exists('media/dbsql/dummy_file.txt')
#     assert course_material.files.all()[0].file.name == 'dbsql/dummy_file.txt'
