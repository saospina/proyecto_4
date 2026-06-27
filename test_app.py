import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_returns_greeting(client):
    response = client.get("/")
    assert b"Hello" in response.data


def test_index_content_type(client):
    response = client.get("/")
    assert response.content_type == "text/html; charset=utf-8"
