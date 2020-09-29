
from src.db import query_db


def test_create_user(test_client):
    username = 'sampleUser'
    response = test_client.post('/createuser', json={
        'username': username,
        'logintoken': '8abcdc42-22ba-4a29-aba7-bd1ebbcc4298',
    })
    assert response.status_code == 200
    assert response.get_json() == dict(success=True)
    existing_users = query_db(
        'SELECT name FROM users WHERE name LIKE ? COLLATE NOCASE', (username, ))
    assert len(existing_users) is 1


def test_create_duplicate_user(test_client):
    username = 'sampleDuplicateUser'
    test_client.post('/createuser', json={
        'username': username,
        'logintoken': '8abcdc42-22ba-4a29-aba7-bd1ebbcc4298',
    })
    response = test_client.post('/createuser', json={
        'username': username,
        'logintoken': '8abcdc42-22ba-4a29-aba7-bd1ebbcc4298',
    })
    assert response.status_code == 409
    assert response.get_json() == dict(
        success=False, error="username is already taken")
    # check to make sure it was not created
    existing_users = query_db(
        'SELECT name FROM users WHERE name LIKE ? COLLATE NOCASE', (username, ))
    assert len(existing_users) is 1


def test_create_user_fail_no_data(test_client):
    response = test_client.post('/createuser')
    assert response.status_code == 400
    assert response.get_json() == dict(success=False, error="400 Bad Request")


def test_create_user_fail_incomplete_data(test_client):
    response = test_client.post('/createuser', json={
        'username': "username",
    })
    assert response.status_code == 400
    assert response.get_json() == dict(success=False, error="400 Bad Request")
