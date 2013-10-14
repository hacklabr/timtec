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
    assert question == response.context_data[u'question']


@pytest.mark.django_db
def test_question_create(rf):
    from core.models import TimtecUser
    from forum.views import QuestionCreateView
    from forum.models import Question
    from core.models import Course

    course = Course.objects.get(slug='dbsql')

    # GET test
    request = rf.get('/forum/question/create/dbsql')
    request.user = TimtecUser.objects.get(username='abcd')

    view = QuestionCreateView(request=request)
    view.kwargs = {'course_slug': 'dbsql'}

    response = view.get(request)
    response.render()
    assert response.status_code == 200
    assert course.name.encode('utf-8') in response.content

    # POST test
    title = 'Test title'
    slug = 'test-title'
    text = 'asljf asdfhuas dfasdflashfdlusafdlsafdlsa filasdflisalfdiayslfdnsalfdyaslifd'

    request = rf.post('/forum/question/create/dbsql', {'title': title, 'text': text})
    request.user = TimtecUser.objects.get(username='abcd')
    view = QuestionCreateView(request=request)
    view.kwargs = {'course_slug': 'dbsql'}
    response = view.post(request)

    question = Question.objects.get(slug=slug)
    assert response.status_code == 302
    assert question.text == text
    assert question.title == title

