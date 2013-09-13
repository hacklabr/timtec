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


@pytest.mark.django_db
def test_question(rf):
    from core.models import TimtecUser
    from forum.views import QuestionView
    from forum.models import Question

    question = Question.objects.get(slug='qual-e-o-melhor-sgbd-atualmente')
    request = rf.get('/forum/question/qual-e-o-melhor-sgbd-atualmente')
    request.user = TimtecUser.objects.get(username='abcd')

    view = QuestionView(request=request)
    view.kwargs = {'slug': 'qual-e-o-melhor-sgbd-atualmente'}

    response = view.get(request)
    response.render()
    assert response.status_code == 200
    assert question.title.encode('utf-8') in response.content
    assert question.text.encode('utf-8') in response.content
    assert question.answers.all()[0].text.encode('utf-8') in response.content
    assert question == response.context_data[u'question']
