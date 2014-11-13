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


@pytest.mark.django_db
def test_question_view_set(user):
    from django.contrib.auth import get_user_model
    from django.test.client import Client
    from forum.serializers import QuestionSerializer
    User = get_user_model()

    professor = User.objects.create_user('professor', 'professor1@test.com', 'password')
    professor2 = User.objects.create_user('professor2', 'professor2@test.com', 'password')

    student1 = mommy.make(User, username='student1', email='test1@test.com')
    student2 = mommy.make(User, username='student2', email='test2@test.com')
    student3 = mommy.make(User, username='student3', email='test3@test.com')
    student4 = mommy.make(User, username='student4', email='test4@test.com')

    course1 = mommy.make('Course', slug='dbsql', name='Test course name')
    course2 = mommy.make('Course', slug='html5', name='Test course name')

    # Test 1: student <user> may see students1 questions (they are from the same class),
    # but not students2 questions (different classes)
    class1 = mommy.make('Class', course=course1, assistant=professor, students=[student1, user])
    class2 = mommy.make('Class', course=course1, assistant=professor2, students=[student2])
    class3 = mommy.make('Class', course=course1, assistant=professor, students=[student3])
    mommy.make('Class', course=course1, assistant=professor, students=[student4])

    question1 = mommy.make('Question', slug='df', course=course1, user=student1)
    question2 = mommy.make('Question', slug='df1', course=course1, user=user)
    question3 = mommy.make('Question', slug='df2', course=course1, user=student2)
    question4 = mommy.make('Question', slug='df3', course=course2, user=student2)

    question5 = mommy.make('Question', slug='df4', course=course1, user=student3)
    mommy.make('Question', slug='df5', course=course1, user=student4)

    student_client = Client()
    student_client.login(username=user.username, password='password')
    response1 = student_client.get('/api/forum_question?course=' + str(course1.id))

    assert QuestionSerializer(question1).data in response1.data
    assert QuestionSerializer(question2).data in response1.data
    assert QuestionSerializer(question3).data not in response1.data
    assert QuestionSerializer(question4).data not in response1.data

    # Test if hidden quesiton are shown only to questions's user
    question1.hidden = True
    question1.save()
    question2.hidden = True
    question2.save()

    response2 = student_client.get('/api/forum_question?course=' + str(course1.id))
    assert QuestionSerializer(question1).data not in response2.data
    assert QuestionSerializer(question2).data in response2.data
    question1.hidden = False
    question1.save()

    # Test if assistant professor can see only his classes questions
    course_professor = mommy.make('CourseProfessor', course=course1, user=professor, role='assistant')
    professor_client = Client()
    professor_client.login(username=professor.username, password='password')
    response3 = professor_client.get('/api/forum_question?course=' + str(course1.id))

    assert QuestionSerializer(question1).data in response3.data
    # this assert test if professor can see hidden question, couse question2 is hidden
    assert QuestionSerializer(question2).data in response3.data
    assert QuestionSerializer(question3).data not in response3.data

    # Test if coordinator professor can see all classes questions
    course_professor.role = 'coordinator'
    course_professor.save()
    response4 = professor_client.get('/api/forum_question?course=' + str(course1.id))
    assert QuestionSerializer(question1).data in response4.data
    # this assert test if professor can see hidden question, couse question2 is hidden
    assert QuestionSerializer(question2).data in response4.data
    assert QuestionSerializer(question3).data in response4.data
    # Test if a question of another course is not feched
    assert QuestionSerializer(question4).data not in response4.data

    course_professor.role = ''
    course_professor.save()
    response5 = professor_client.get('/api/forum_question?course=' + str(course1.id))
    assert len(response5.data) == 0

    # Test filter by classes passed as GET parameters
    # http://localhost:8000/api/course_stats/1?classes=17&classes=6
    course_professor.role = 'assistant'
    course_professor.save()
    response6 = professor_client.get('/api/forum_question?course=' +
                                     str(course1.id) + "&classes=" +
                                     str(class1.id) + "&classes=" +
                                     str(class2.id) + "&classes=" +
                                     str(class3.id))
    assert QuestionSerializer(question1).data in response6.data
    assert QuestionSerializer(question2).data in response6.data
    assert QuestionSerializer(question3).data not in response6.data
    assert QuestionSerializer(question4).data not in response6.data
    assert QuestionSerializer(question5).data in response6.data

    # Test if professor group menber can see all classes questions
    # course_professor.role = ''
    # course_professor.save()
    # professors_group = mommy.make('Group', name='professor')
    # professor.groups.add(professors_group)
    # response4 = client2.get('/api/forum_question?course=' + str(course1.id))
    # assert QuestionSerializer(question1).data in response4.data
    # # this assert test if professor can see hidden question, couse question2 is hidden
    # assert QuestionSerializer(question2).data in response4.data
    # assert QuestionSerializer(question3).data not in response4.data
