import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_forum(admin_client, user):
    course = mommy.make('Course', slug='dbsql')
    mommy.make('Lesson', course=course, slug='lesson')
#     question = mommy.make('Question', slug='qual-e-o-melhor-sgbd-atualmente', title='Test Question', text='Test Question 1234 Test Question 1234', course=course)

    response = admin_client.get('/forum/dbsql/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_question(admin_client, user):

    course = mommy.make('Course')
    mommy.make('Lesson', course=course, slug='lesson')
    question = mommy.make('Question', slug='df', course=course)

    response = admin_client.get('/forum/question/' + question.slug + '/')

    assert response.status_code == 200
    assert question == response.context_data[u'question_django']


@pytest.mark.django_db
def test_question_create(admin_client, user):
    from forum.models import Question

    course = mommy.make('Course', slug='dbsql', name='Test course name')
    mommy.make('Lesson', course=course, slug='lesson')

    # GET test
    response = admin_client.get('/forum/question/add/dbsql/')

    assert response.status_code == 200
    assert course.name.encode('utf-8') in response.content

    # POST test
    title = 'Test title'
    slug = 'test-title'
    text = 'asljf asdfhuas dfasdflashfdlusafdlsafdlsa filasdflisalfdiayslfdnsalfdyaslifd'

    response = admin_client.post('/forum/question/add/dbsql/', {'title': title, 'text': text})

    assert response.status_code == 302
    question = Question.objects.get(slug=slug)
    assert question.text == text
    assert question.title == title
