import datetime
import time
import pytest
from app import app, db


@pytest.fixture
def client():
    app.config.from_object('app.config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_register(client):
    data = {
        "username": "testuser1",
        "email": "testuser@example.com"
    }

    response = client.post('/user', json=data)

    assert response.status_code == 201
    assert response.get_json()["username"] == "testuser1"
    assert response.get_json()["email"] == "testuser@example.com"


def test_get_user_by_email(client):
    data = {
        "username": "anotheruser",
        "email": "anotheruser@example.com"
    }
    client.post('/user', json=data)

    response = client.get('/user/email/anotheruser@example.com')

    assert response.status_code == 200
    assert response.get_json()["username"] == "anotheruser"
    assert response.get_json()["email"] == "anotheruser@example.com"


def test_get_all_users(client):
    client.post('/user', json={"username": "user1", "email": "user1@example.com"})
    client.post('/user', json={"username": "user2", "email": "user2@example.com"})

    response = client.get('/user')

    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_delete_user(client):
    data = {
        "username": "deleteuser",
        "email": "deleteuser@example.com"
    }
    client.post('/user', json=data)

    response = client.delete('/user/deleteuser@example.com')

    assert response.status_code == 200


def test_delete_non_existing_user(client):
    response = client.delete('/user/nonexistent@example.com')
    assert response.status_code == 404


def test_put_user(client):
    data = {
        "username": "user",
        "email": "user@example.com"
    }
    client.post('/user', json=data)

    data = {
        "username": "user123",
        "email": "user123@example.com"
    }
    response = client.put('/user/user@example.com', json=data)

    expected_data = {
        "id": response.get_json()["id"],
        "email": "user123@example.com",
        "username": "user123",
        "created_at": response.get_json()["created_at"]
    }

    assert response.get_json() == expected_data
    assert response.status_code == 200

    response = client.get('/user/email/user123@example.com')

    assert response.get_json() == expected_data
    assert response.status_code == 200


def test_get_user_by_datetime(client):
    data = {
        "username": "user",
        "email": "user@example.com"
    }
    client.post('/user', json=data)

    created_at = datetime.datetime.utcnow()
    start_time = created_at - datetime.timedelta(seconds=5)
    end_time = created_at + datetime.timedelta(seconds=1)
    time.sleep(3)

    data = {
        "username": "user123",
        "email": "user@example.com"
    }

    client.post('/user', json=data)

    response = client.get(f'/user/{start_time.strftime("%Y-%m-%dT%H:%M:%S")}/{end_time.strftime("%Y-%m-%dT%H:%M:%S")}')

    expected_data = {
        "id": 1,
        "email": "user@example.com",
        "username": "user",
        "created_at": response.get_json()[0]["created_at"]
    }

    assert response.get_json()[0] == expected_data
    assert response.status_code == 200


def test_get_user_by_username_and_by_time(client):
    data = {
        "username": "user",
        "email": "user@example.com"
    }
    client.post('/user', json=data)

    data = {
        "username": "user123",
        "email": "user123@example.com"
    }

    client.post('/user', json=data)

    response = client.get(f'/user/user/2000-01-01T12:00:00/2200-01-01T12:00:00')

    expected_data = {
        "id": 1,
        "email": "user@example.com",
        "username": "user",
        "created_at": response.get_json()[0]["created_at"]
    }

    assert response.get_json()[0] == expected_data
    assert response.status_code == 200
