import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_enroll_user_view(rf, user):
    from core.models import Course
    from core.views import EnrollCourseView
    import datetime

    course = mommy.make('Course', slug='acceptance_enroll_user', start_date=datetime.date.today(), status='published')
    lesson = mommy.make('Lesson', course=course, slug='lesson')

    request = rf.get('/courses/' + course.slug + '/enroll/')
    request.user = user

    view = EnrollCourseView(request=request)
    view.kwargs = {'slug': course.slug}

    assert view.get_object().id == Course.objects.get(slug=course.slug).id

    response = view.get(request)
    assert response.status_code == 302
    assert response['Location'] == '/course/' + course.slug + '/lesson/' + lesson.slug + '/'


@pytest.mark.django_db
def test_home_view(rf):
    from core.views import HomeView

#     course = mommy.make('Course')

    request = rf.get('/')
    view = HomeView(request=request)

    response = view.get(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_view(rf, user):
    from accounts.views import ProfileView

    request = rf.get('/profile/')
    request.user = user
    view = ProfileView(request=request)
    response = view.get(request)
    assert response.status_code == 200
    assert response.context_data['profile_user'].username == user.username

    request = rf.get('/profile/abcd')
    request.user = user
    view = ProfileView(request=request)
    view.kwargs = {'username': user.username}
    response = view.get(request)
    assert response.status_code == 200
    assert response.context_data['profile_user'].username == user.username

    request = rf.get('/profile/1234')
    request.user = user
    view = ProfileView(request=request)
    view.kwargs = {'username': '1234'}
    response = view.get(request)
    assert response.status_code == 200
    assert response.context_data['profile_user'].username == user.username
