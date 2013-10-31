import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_forum(rf, user):
    from forum.views import CourseForumView

    course = mommy.make('Course', slug='dbsql')
    mommy.make('Lesson', course=course)
    question = mommy.make('Question', slug='qual-e-o-melhor-sgbd-atualmente', title='Test Question', text='Test Question 1234 Test Question 1234', course=course)

    request = rf.get('/forum/dbsql')
    request.user = user

    view = CourseForumView(request=request)
    view.kwargs = {'course_slug': 'dbsql'}

    response = view.get(request)
    response.render()
    assert response.status_code == 200
    assert question.title.encode('utf-8') in response.content
    # restrict text size to avoid /n, couse they are converted to <br> in response.content making the test fail.
    assert question.text[0:200].encode('utf-8') in response.content
    assert set([question]) == set(response.context_data[u'questions'])


@pytest.mark.django_db
def test_question(rf, user):
    from forum.views import QuestionView

    course = mommy.make('Course')
    mommy.make('Lesson', course=course)
    question = mommy.make('Question', slug='df', course=course)

    request = rf.get('/forum/question/' + question.slug)
    request.user = user

    view = QuestionView(request=request)
    view.kwargs = {'slug': question.slug}

    response = view.get(request)
    response.render()
    assert response.status_code == 200
    assert question.title.encode('utf-8') in response.content
    assert question.text.encode('utf-8') in response.content
    assert question == response.context_data[u'question']


@pytest.mark.django_db
def test_question_create(rf, user):
    from forum.views import QuestionCreateView
    from forum.models import Question

    course = mommy.make('Course', slug='dbsql', name='Test course name')
    mommy.make('Lesson', course=course)

    # GET test
    request = rf.get('/forum/question/create/dbsql')
    request.user = user

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
    request.user = user
    view = QuestionCreateView(request=request)
    view.kwargs = {'course_slug': 'dbsql'}
    response = view.post(request)

    question = Question.objects.get(slug=slug)
    assert response.status_code == 302
    assert question.text == text
    assert question.title == title
