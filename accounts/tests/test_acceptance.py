import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_custom_login_view(client, user):
    response = client.get('/login/')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated() is False

    response = client.post('/login/', {'username': user.username,
                                       'password': 'password'})
    assert response.status_code == 302

    course = mommy.make('Course')
    response = client.get('/course/' + course.slug + '/')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated()


@pytest.mark.django_db
def test_custom_login_view_email_verification(client, user):
    from allauth.account.models import EmailAddress
    mommy.make('Group', name="students")
    response = client.get('/accounts/signup/')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated() is False

    response = client.post('/accounts/signup/', {'username': "test", 'email': "test@example.com",
                                                 'password1': 123123, 'password2': 123123, "accept_terms": True})

    assert response.status_code == 302

    response = client.post('/login/', {'username': "test",
                                       'password': '123123'})
    assert response.status_code == 302

    response = client.get('/login/')
    assert response.context['request'].user.is_authenticated() is False

    ea = EmailAddress.objects.get(email="test@example.com")
    ea.verified = True
    ea.save()
    response = client.post('/login/', {'username': "test",
                                       'password': '123123'})
    course = mommy.make('Course')
    response = client.get('/course/' + course.slug + '/')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated()


@pytest.mark.django_db
def test_custom_login_view_with_next_field(client, user):
    response = client.get('/login/')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated() is False

    response = client.post('/login/', {'username': user.username,
                                       'password': 'password',
                                       'next': '/profile/edit'})
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/profile/edit'


@pytest.mark.django_db
def test_custom_login_redirect_already_authenticated_user(client, user):
    response = client.post('/login/', {'username': user.username, 'password': 'password'})
    assert response.status_code == 302

    response = client.get('/login/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_custom_login_page(client):
    response = client.get('/login/', {'next': 'http://fakenext.com/profile/edit'})

    assert response.status_code == 200
    assert 'login' in response.content


@pytest.mark.django_db
def test_custom_login_does_not_redirect_to_unsafe_next(admin_client):
    response = admin_client.get('/login/', {'next': 'http://fakenext.com/profile/edit'})

    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'


@pytest.mark.django_db
def test_custom_login_has_login_form_in_context_when_login_fail(client):
    response = client.post('/login/', {'username': 'invalid',
                                       'password': 'invalid'})

    assert response.status_code == 200
    assert 'login_form' in response.context_data


@pytest.mark.django_db
def test_user_instance_for_profile_edit_form_is_the_same_of_request(client, user):
    response = client.post('/login/', {'username': user.username, 'password': 'password'})

    response = client.get('/profile/edit')
    assert response.status_code == 200
    assert response.context_data['form'].instance.username == user.username


@pytest.mark.django_db
def test_edit_profile(admin_client):
    response = admin_client.post('/profile/edit', {'username': 'admin', 'email': 'admin@b.cd'})

    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/profile/'


def test_admin_user(admin_client):
    response = admin_client.get('/django/admin/accounts/timtecuser/?q=admin')
    assert 'admin' in response.content


@pytest.mark.django_db
def test_username_login(client, user):
    response = client.post('/login/', {'username': user.username, 'password': 'password'})
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'


@pytest.mark.django_db
def test_email_login(client, user):
    response = client.post('/login/', {'username': user.email, 'password': 'password'})
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/'


@pytest.mark.django_db
def test_next_field_still_works(client, user):
    reponse = client.post('/login/', {'username': user.email, 'password': 'password', 'next': '/profile/edit'})
    assert reponse.status_code == 302
    assert reponse['Location'] == 'http://testserver/profile/edit'
