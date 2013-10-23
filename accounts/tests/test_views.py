import pytest


@pytest.mark.django_db
def test_enroll_user_view(rf):
    from core.models import Course, TimtecUser
    from core.views import EnrollCourseView

    request = rf.get('/courses/dbsql/enroll')
    request.user = TimtecUser.objects.get(username='abcd')

    view = EnrollCourseView(request=request)
    view.kwargs = {'slug': 'dbsql'}

    assert view.get_object().id == Course.objects.get(slug='dbsql').id

    response = view.get(request)
    assert response.status_code == 302
    assert response['Location'] == '/lesson/aula-1-modelos-de-dados-e-introducao-ao-modelo-relacional'


@pytest.mark.django_db
def test_home_view(rf):
    from core.views import HomeView

    request = rf.get('/')
    view = HomeView(request=request)

    response = view.get(request)
    assert response.status_code == 302
    assert response['Location'] == '/course/dbsql'


@pytest.mark.django_db
def test_profile_view(rf):
    from core.models import TimtecUser
    from accounts.views import ProfileView

    request = rf.get('/profile/')
    request.user = TimtecUser.objects.get(username='abcd')
    view = ProfileView(request=request)
    response = view.get(request)
    assert response.status_code == 200
    assert response.context_data['profile_user'].username == 'abcd'

    request = rf.get('/profile/abcd')
    request.user = TimtecUser.objects.get(username='abcd')
    view = ProfileView(request=request)
    view.kwargs = {'username': 'abcd'}
    response = view.get(request)
    assert response.status_code == 200
    assert response.context_data['profile_user'].username == 'abcd'

    request = rf.get('/profile/1234')
    request.user = TimtecUser.objects.get(username='abcd')
    view = ProfileView(request=request)
    view.kwargs = {'username': '1234'}
    response = view.get(request)
    assert response.status_code == 200
    assert response.context_data['profile_user'].username == 'abcd'
