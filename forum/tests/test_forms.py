import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_question_form(user):
    from forum.forms import QuestionForm
    from forum.models import Question

    instance = Question()
    instance.course = mommy.make('Course', slug='dbsql')
    instance.user = user

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
