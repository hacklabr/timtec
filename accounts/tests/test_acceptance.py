import pytest

@pytest.mark.django_db
def test_custom_login_view(client):
    response = client.get('/login/')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated() is False

    response = client.post('/login/', {'username':'abcd',
                                       'password': 'x'})
    assert response.status_code == 302

    response = client.get('/course/dbsql')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated()


@pytest.mark.django_db
def test_custom_login_view_with_next_field(client):
    response = client.get('/login/')
    assert response.status_code == 200
    assert response.context['request'].user.is_authenticated() is False

    response = client.post('/login/', {'username':'abcd',
                                       'password': 'x',
                                       'next': '/profile/edit'})
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/profile/edit'


@pytest.mark.django_db
def test_custom_login_redirect_already_authenticated_user(client):
    response = client.post('/login/', {'username':'abcd', 'password': 'x'})
    assert response.status_code == 302

    response = client.get('/login/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_custom_login_does_not_redirect_to_unsafe_next(client):
    response = client.post('/login/', {'username':'abcd',
                                       'password': 'x',
                                       'next': 'http://fakenext.com/profile/edit'})

    assert response.status_code == 302
    assert response['Location'].startswith('http://testserver/')


@pytest.mark.django_db
def test_custom_login_has_login_form_in_context_when_login_fail(client):
    response = client.post('/login/', {'username':'invalid',
                                       'password': 'invalid'})

    assert response.status_code == 200
    assert 'login_form' in response.context_data


@pytest.mark.django_db
def test_user_instance_for_profile_edit_form_is_the_same_of_request(client):
    response = client.post('/login/', {'username':'abcd', 'password': 'x',})

    response = client.get('/profile/edit')
    assert response.status_code == 200
    assert response.context_data['form'].instance.username == 'abcd'

