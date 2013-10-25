import pytest


@pytest.mark.django_db
def test_question_form():
    from core.models import TimtecUser
    from forum.forms import QuestionForm
    from core.models import Course
    from forum.models import Question

    instance = Question()
    instance.course = Course.objects.get(slug='dbsql')
    instance.user = TimtecUser.objects.get(username='abcd')

    data = {
        'title': 'Test Title',
        'text': 'asljf asdfhuas dfasdflashfdlusafdlsafdlsa filasdflisalfdiayslfdnsalfdyaslifd',
    }

    form = QuestionForm(instance=instance, data=data)
    assert form.is_valid() is True, form.errors
    form.save()
    assert Question.objects.filter(slug='test-title').exists()

    data = {
        'title': '',
        'text': 'asljf asdfhuas dfasdflashfdlusafdlsafdlsa filasdflisalfdiayslfdnsalfdyaslifd',
    }
    form = QuestionForm(data=data)
    assert form.is_valid() is False

    data = {
        'title': 'Test Title',
        'text': '',
    }
    form = QuestionForm(data=data)
    assert form.is_valid() is False
