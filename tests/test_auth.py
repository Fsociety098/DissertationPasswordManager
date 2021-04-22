import pytest
import PasswordManager
from flask import g, session


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'fName': 'test', 'userEmail': 'test2@test.com', 'userConfirm': 'test2@test.com',
                                'secureKey': 'secureKey2', 'password': 'test@Password12',
                                'passwordConfirm': 'test@Password12'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert PasswordManager.db.get_db().execute(
            "select * from user where fName = 'test'",
        ).fetchone() is not None


@pytest.mark.parametrize(('message', 'fName', 'userEmail', 'userConfirm', 'secureKey', 'password', 'passwordConfirm'), (
        (b'Full name is required', '', '', '', '', '', ''),
        (b'Email Address is required', 'test', '', '', '', '', ''),
        (b'Confirm Email Address is required', 'test', 'test@test.com', '', '', '', ''),
        (b'Your emails do not match', 'test', 'test@test.com', 'test1@test.com', '', '', ''),
        (b'Your emails do not match', 'test', 'test1@test.com', 'test@test.com', '', '', ''),
        (b'A secure Key is required', 'test', 'test@test.com', 'test@test.com', '', '', ''),
        (b'Password is required', 'test', 'test@test.com', 'test@test.com', 'secureKey', '', ''),
        (b'Your password must be greater than 8 characters', 'test', 'test@test.com', 'test@test.com', 'secureKey',
         'pass', ''),
        (b'Your password must', 'test', 'test@test.com', 'test@test.com', 'secureKey', 'password1', ''),
        (b'Your passwords do not match', 'test', 'test@test.com', 'test@test.com', 'secureKey', 'password1@A', 'pass1'),
        (b'is already registered', 'test', 'test@test.com', 'test@test.com', 'secureKey', 'password1@A', 'password1@A'),
))
def test_register_validate_input(client, fName, userEmail, userConfirm, secureKey, password, passwordConfirm, message):
    response = client.post(
        '/auth/register',
        data={'fName': fName, 'userEmail': userEmail, 'userConfirm': userConfirm, 'secureKey': secureKey,
              'password': password, 'passwordConfirm': passwordConfirm}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['fName'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('a', 'test', b'Incorrect username.'),
        ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
