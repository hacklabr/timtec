import pytest


@pytest.mark.django_db
def test_forum(rf):
    from core.models import TimtecUser
    from forum.views import CourseForumView
    from forum.models import Question

    questions = Question.objects.filter(course__slug='dbsql')
    request = rf.get('/forum/dbsql')
    request.user = TimtecUser.objects.get(username='abcd')

    view = CourseForumView(request=request)
    view.kwargs = {'course_slug': 'dbsql'}

    response = view.get(request)
    response.render()
    assert response.status_code == 200
    assert questions[0].title.encode('utf-8') in response.content
    assert questions[0].text.encode('utf-8') in response.content
    assert set(questions) == set(response.context_data[u'questions'])
