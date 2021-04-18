import pytest
import app as app

@pytest.fixture
def app():
    yield app


@pytest.fixture
def client(app):
    return app.test_client()