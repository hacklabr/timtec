# -*- coding: utf-8 -*-
import pytest
from model_mommy import mommy

from conftest import create_user
from core.models import Class, Course


@pytest.mark.django_db
def test_lesson(admin_client):
    lesson = mommy.make('Lesson', slug='lesson', status='published')
    response = admin_client.get('/course/' + lesson.course.slug + '/lesson/' + lesson.slug + '/')
    assert response.status_code == 200
    assert lesson.name.encode('utf-8') in response.content


def assign_professor_to_course(course, existing_professor=None, new_professor_username=None, role=None):
    """

    :param existing_professor: Existing object TimtecUser
    :param new_professor_user_name: Non-existing professor username, if not defined, it will be created
    :param course: The course to assign professor to
    :param role: Role to assign to professor
    :return: The created/existing professor
    """

    if existing_professor is not None:
        professor = existing_professor
    else:
        professor = create_user(new_professor_username)

    mommy.make('CourseProfessor', user=professor, course=course, role=role)

    return professor


@pytest.mark.django_db
def test_assistant_professor_cannot_change_class_professor(client):
    course = mommy.make('Course', slug='dbsql', name='Test course name')

    coordinator_professor = assign_professor_to_course(course, new_professor_username='coordinator_professor',
                                                       role='coordinator')

    assistant_professor = assign_professor_to_course(course, new_professor_username='assistant_professor',
                                                     role='assistant')

    another_assistant = assign_professor_to_course(course, new_professor_username='another_assistant', role='assistant')

    klass = mommy.make('Class', name='Test class name', course=course, assistant=coordinator_professor)

    client.login(username=assistant_professor.username, password='password')

    response = client.post('/class/' + str(klass.id) + '/', {'name': 'A class', 'assistant': another_assistant.id})

    assert response.status_code == 403


@pytest.mark.django_db
def test_coordinator_professor_can_change_class_professor(client):
    course = mommy.make('Course', slug='dbsql', name='Test course name')

    coordinator_professor = assign_professor_to_course(course, new_professor_username='coordinator_professor',
                                                       role='coordinator')

    assistant_professor = assign_professor_to_course(course, new_professor_username='assistant_professor',
                                                     role='assistant')

    another_assistant = assign_professor_to_course(course, new_professor_username='another_assistant', role='assistant')

    klass = mommy.make('Class', name='A class', course=course, assistant=assistant_professor)

    client.login(username=coordinator_professor.username, password='password')

    response = client.post('/class/' + str(klass.id) + '/', {'name': 'A class', 'assistant': another_assistant.id})

    # A página redireciona para outro lugar em caso de sucesso
    assert response.status_code == 302

    changed_class = Class.objects.get(id=klass.id)

    assert changed_class.assistant == another_assistant


@pytest.mark.django_db
def test_assistant_professor_can_change_other_data_than_professor_on_its_own_class(client):
    course = mommy.make('Course', slug='dbsql', name='Another course')

    assign_professor_to_course(course, new_professor_username='coordinator_professor', role='coordinator')

    assistant_professor = assign_professor_to_course(course, new_professor_username='assistant_professor',
                                                     role='assistant')

    klass = mommy.make('Class', name='Old class name', course=course, assistant=assistant_professor)

    client.login(username=assistant_professor.username, password='password')

    response = client.post('/class/' + str(klass.id) + '/',
                           {'name': 'New class name', 'assistant': assistant_professor.id})

    # A página redireciona para outro lugar em caso de sucesso
    assert response.status_code == 302

    changed_class = Class.objects.get(id=klass.id)

    assert changed_class.name == 'New class name'


@pytest.mark.django_db
def test_get_courses_user_has_role(client):
    course = mommy.make('Course', slug='dbsql', name='A course')

    another_course = mommy.make('Course', slug='mysql', name='Another course')

    course_whose_professor_coordinate = mommy.make('Course', slug='coordinatedcourse',
                                                   name='Course whose professor coordinate')

    another_course_whose_professor_coordinate = mommy.make('Course', slug='anothercoordinatedcourse',
                                                           name='Another course whose professor coordinate')

    professor1 = assign_professor_to_course(course, new_professor_username='professor1', role='assistant')

    assign_professor_to_course(another_course, existing_professor=professor1, role='assistant')

    assign_professor_to_course(course_whose_professor_coordinate, existing_professor=professor1, role='coordinator')

    assign_professor_to_course(another_course_whose_professor_coordinate, existing_professor=professor1,
                               role='coordinator')

    client.login(username=professor1.username, password='password')

    response = client.get('/my-courses/')

    assert response.status_code == 200

    courses_user_assist = response.context[-1]['courses_user_assist']

    assert courses_user_assist

    courses_user_coordinate = response.context[-1]['courses_user_coordinate']

    assert courses_user_coordinate


@pytest.mark.django_db
def test_cannot_remove_courses_default_class(admin_client):
    course = mommy.make('Course', slug='mysql', name='A course')

    klass = course.default_class

    response = admin_client.post('/class/' + str(klass.id) + '/delete/')

    assert response.status_code == 403

    assert Class.objects.filter(id=klass.id).exists()

    assert Course.objects.filter(id=course.id).exists()


@pytest.mark.django_db
def test_course_average_lessons_users_progress_should_return_zero_with_no_students_on_course():
    course = mommy.make('Course', slug='dbsql', name='A course')

    lesson1 = mommy.make('Lesson', course=course, slug='lesson1')

    mommy.make('Lesson', course=course, slug='lesson2')

    mommy.make('Unit', lesson=lesson1, title='Title 1')

    progress_list = course.avg_lessons_users_progress()

    assert progress_list[0]['slug'] == 'lesson1'

    assert progress_list[0]['progress'] == 0

    assert progress_list[1]['slug'] == 'lesson2'

    assert progress_list[1]['progress'] == 0


@pytest.mark.django_db
def test_user_courses_cannot_show_assistant_and_coordinator_tabs_for_students(client):
    student = create_user('student')

    client.login(username=student.username, password='password')

    response = client.get('/my-courses/')

    assert 'href="#course-as-teacher"' not in response.content

    assert 'href="#course-as-coordinator"' not in response.content


@pytest.mark.django_db
def test_user_courses_must_show_assistant_tab_for_assistant(client):
    course = mommy.make('Course', slug='dbsql', name='A course')

    professor = assign_professor_to_course(course, new_professor_username='assistant_professor', role='assistant')

    client.login(username=professor.username, password='password')

    response = client.get('/my-courses/')

    assert 'href="#course-as-teacher"' in response.content

    assert 'href="#course-as-coordinator"' not in response.content


@pytest.mark.django_db
def test_user_courses_must_show_coordinator_tab_for_coordinator(client):
    course = mommy.make('Course', slug='dbsql', name='A course')

    professor = assign_professor_to_course(course, new_professor_username='coordinator_professor', role='coordinator')

    client.login(username=professor.username, password='password')

    response = client.get('/my-courses/')

    assert 'href="#course-as-teacher"' not in response.content

    assert 'href="#course-as-coordinator"' in response.content


@pytest.mark.django_db
def test_user_courses_must_show_assistant_and_coordinator_tabs_for_assistant_and_coordinator_professor(client):
    course_assisted = mommy.make('Course', slug='dbsql', name='Assisted course')

    professor = assign_professor_to_course(course_assisted, new_professor_username='professor', role='assistant')

    course_coordinated = mommy.make('Course', slug='coordinatedcourse', name='Coordinated course')

    assign_professor_to_course(course_coordinated, existing_professor=professor, role='coordinator')

    client.login(username=professor.username, password='password')

    response = client.get('/my-courses/')

    assert 'href="#course-as-teacher"' in response.content

    assert 'href="#course-as-coordinator"' in response.content


@pytest.mark.django_db
def test_course_professor_get_bio_or_pic_should_be_user_bio__or_pic_when_not_defined(admin_client):
    course = mommy.make('Course', slug='dbsql', name='A course')

    professor = create_user('professor')

    professor.biography = 'Professor Biography'

    # professor.picture = 'Some valid image'

    course_professor = mommy.make('CourseProfessor', user=professor, course=course, role='assistant')
    # course_professor = mommy.make('CourseProfessor', user=professor, course=course, picture=?, role='assistant')

    assert course_professor.get_biography() == 'Professor Biography'

    # assert course_professor.get_picture() == 'Same image as above'


@pytest.mark.django_db
def test_course_professor_get_bio_or_pic_should_be_course_professor_bio_or_pic_when_defined(admin_client):
    course = mommy.make('Course', slug='dbsql', name='A course')

    professor = create_user('professor')

    professor.biography = 'Professor Biography'

    # professor.picture = 'Some valid image'

    course_professor = mommy.make('CourseProfessor', user=professor, course=course, role='assistant')

    course_professor.biography = 'Course professor Biography'

    # course_professor.picture = 'Another valid image'

    assert course_professor.get_biography() == 'Course professor Biography'

    # assert course_professor.get_picture() == 'Course professor Picture'


@pytest.mark.django_db
def test_only_admin_or_coordinator_can_edit_course(client, admin_client):
    course = mommy.make('Course', slug='dbsql', name='A course', abstract='asdf')

    professor = create_user('professor')
    client.login(username=professor.username, password='password')

    response = client.post('/api/course/' + str(course.id), {'id': str(course.id),
                                                             'slug': course.slug,
                                                             'abstract': 'A abstract'})
    assert response.status_code == 403
    assert course.abstract == 'asdf'

    mommy.make('CourseProfessor', user=professor, course=course, role='coordinator')
    response = client.post('/api/course/' + str(course.id), {'id': str(course.id),
                                                             'slug': course.slug,
                                                             'abstract': 'A abstract'})

    changed_course = Course.objects.get(id=course.id)
    assert response.status_code == 200
    assert changed_course.abstract == 'A abstract'

    response = admin_client.post('/api/course/' + str(course.id), {'id': str(course.id),
                                                                   'slug': course.slug,
                                                                   'abstract': 'Another abstract'})
    changed_course = Course.objects.get(id=course.id)
    assert response.status_code == 200
    assert changed_course.abstract == 'Another abstract'


#  FIXME: Bad Request (400) and Regration case after upgrade to Rest Framework 3.3.0: http://stackoverflow.com/questions/33441197/django-rest-framework-browsable-api-form-always-returns-400-bad-request
@pytest.mark.django_db
def test_only_admin_or_coordinator_can_edit_courseprofessors(client, admin_client):
    from core.models import CourseProfessor
    import json

    course = mommy.make('Course', slug='dbsql', name='A course', abstract='asdf')

    professor = create_user('professor')
    course_professor = mommy.make('CourseProfessor', course=course, biography='asdf')
    client.login(username=professor.username, password='password')

    response = client.put('/api/course_professor/' + str(course_professor.id),
                          {'id': str(course_professor.id),
                           'biography': 'A biography'},
                          content_type='application/json;charset=UTF-8')
    assert response.status_code == 403
    assert course_professor.biography == 'asdf'

    # set user as coordinator
    mommy.make('CourseProfessor', user=professor, course=course, role='coordinator')
    response = client.put('/api/course_professor/' + str(course_professor.id),
                          json.dumps({'id': str(course_professor.id),
                                      'course': course.id,
                                      'professor': professor.id,
                                      'biography': 'A biography'}),
                          content_type='application/json;charset=UTF-8')
    changed_course_professor = CourseProfessor.objects.get(id=course_professor.id)

    assert response.status_code == 200
    assert changed_course_professor.biography == 'A biography'

    response = admin_client.put('/api/course_professor/' + str(course_professor.id),
                                json.dumps({'id': str(course_professor.id),
                                            'course': course.id,
                                            'biography': 'Another biography as admin'}),
                                content_type='application/json;charset=UTF-8')
    changed_course_professor = CourseProfessor.objects.get(id=course_professor.id)
    assert response.status_code == 200
    assert changed_course_professor.biography == 'Another biography as admin'
