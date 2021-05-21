from PasswordManager import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(client):
    response = client.get('/')
    assert b'<div id="myCarousel" class="carousel slide carousel-height" data-bs-ride="carousel">' in response.data
