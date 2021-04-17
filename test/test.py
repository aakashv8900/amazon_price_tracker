import pytest

import app as flask_app

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

def test_redirection(app,client):
    print(client)
    # checking redirection
    response = client.get("/")
    assert response.status_code == 200