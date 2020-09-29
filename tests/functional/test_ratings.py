
from src.db import query_db


def test_create_rating_fail_no_data(test_client):
    response = test_client.post('/ratings/sample.app/add')
    assert response.status_code == 400
    assert response.get_json() == dict(success=False, error="400 Bad Request")


def test_create_rating_fail_incomplete_data(test_client):
    response = test_client.post('/ratings/sample.app/add', json={
        'username': "username",
        'logintoken': "8abcdc42",
        'points': 2
    })
    assert response.status_code == 400
    assert response.get_json() == dict(success=False, error="400 Bad Request")
    response = test_client.post('/ratings/sample.app/add', json={
        'username': "username",
        'logintoken': "8abcdc42",
        'description': "very good app"
    })
    assert response.status_code == 400
    assert response.get_json() == dict(success=False, error="400 Bad Request")


def test_create_rating_fail_invalid_user(test_client):
    response = test_client.post('/ratings/sample.app/add', json={
        'username': "username",
        'logintoken': "8abcdc42",
        'points': 2,
        'description': "very good app"
    })
    assert response.status_code == 401
    assert response.get_json() == dict(success=False, error="user not found")


def createTestUser(test_client, username, logintoken):
    # helper function to create a user for testing
    response = test_client.post('/createuser', json={
        'username': username,
        'logintoken': logintoken,
    })
    assert response.status_code == 200
    assert response.get_json() == dict(success=True)
    existing_users = query_db(
        'SELECT name FROM users WHERE name LIKE ? COLLATE NOCASE', (username, ))
    assert len(existing_users) is 1


def test_create_rating_fail_description(test_client):
    # create user
    username = 'fail_description'
    logintoken = '71ffda91-1eb2-47dc-8e30-189ac6eb3050'
    createTestUser(test_client, username, logintoken)
    # the test
    response = test_client.post('/ratings/sample.app/add', json={
        'username': username,
        'logintoken': logintoken,
        'points': 2,
        'description': "hi"
    })
    assert response.status_code == 400
    assert response.get_json() == dict(
        success=False, error="review description is to short")


def test_create_rating_points_out_of_range(test_client):
    # create user
    username = 'points_out_of_range'
    logintoken = '71ffda91-1eb2-47dc-8e30-189ac6eb3050'
    createTestUser(test_client, username, logintoken)
    # the test

    def test_invalid_points(invalid_points):
        response = test_client.post('/ratings/sample.app/add', json={
            'username': username,
            'logintoken': logintoken,
            'points': invalid_points,
            'description': "fine"
        })
        assert response.status_code == 400
        assert response.get_json() == dict(
            success=False, error="rating can only be between 1 and 5")

    test_invalid_points(10)
    test_invalid_points(100)
    test_invalid_points(-10)
    test_invalid_points(0)
    test_invalid_points(-1)
    test_invalid_points(6)


def test_create_rating_points_not_a_number(test_client):
    # create user
    username = 'points_not_a_number'
    logintoken = '51ffda91-1eb2-47dc-8e30-189ac6eb3050'
    createTestUser(test_client, username, logintoken)
    # the test

    response = test_client.post('/ratings/sample.app/add', json={
        'username': username,
        'logintoken': logintoken,
        'points': "t",
        'description': "fine"
    })
    assert response.status_code == 400
    assert response.get_json() == dict(
        success=False, error="value error, is your rating a number?")


def test_create_rating_success_and_view(test_client):
    # create user
    username = 'points_sucess'
    logintoken = '41ffda91-1eb2-47dc-8e30-189ac6eb3050'
    createTestUser(test_client, username, logintoken)
    # the test
    # create rating
    response = test_client.post('/ratings/sample.app1/add', json={
        'username': username,
        'logintoken': logintoken,
        'points': 5,
        'description': "an essential app for everyone"
    })
    assert response.status_code == 201
    assert response.get_json() == dict(success=True)
    # check if it is in the list of ratings
    response = test_client.get('/ratings/sample.app1')
    assert response.status_code == 200
    result = response.get_json()
    ratings = result["ratings"]
    assert len(ratings) == 1
    assert ratings[0]["description"] == "an essential app for everyone"
    assert ratings[0]["username"] == username
    assert ratings[0]["points"] == 5


def test_create_multiple_ratings_and_view(test_client):
    def create_user_and_rating(test_client, username, points, description):
        logintoken = '41ffda91-1eb2-47dc-8e30-189ac6eb3050'
        createTestUser(test_client, username, logintoken)
        response = test_client.post('/ratings/sample.app2/add', json={
            'username': username,
            'logintoken': logintoken,
            'points': points,
            'description': description
        })
        assert response.status_code == 201
        assert response.get_json() == dict(success=True)
    # create test data
    create_user_and_rating(
        test_client, "multiple_ratings_user1", 4, "test description1")
    create_user_and_rating(
        test_client, "multiple_ratings_user2", 1, "test description2")
    create_user_and_rating(
        test_client, "multiple_ratings_user3", 3, "test description3")
    # check the list of ratings
    response = test_client.get('/ratings/sample.app2')
    assert response.status_code == 200
    result = response.get_json()
    assert result["appid"] == "sample.app2"
    assert result["average"] == 2.6666666666666665  # (4+1+3)/3
    ratings = result["ratings"]
    assert len(ratings) == 3
    # testing each ratings, the order should be newest first
    assert ratings[2]["username"] == "multiple_ratings_user1"
    assert ratings[2]["points"] == 4
    assert ratings[2]["description"] == "test description1"

    assert ratings[1]["username"] == "multiple_ratings_user2"
    assert ratings[1]["points"] == 1
    assert ratings[1]["description"] == "test description2"

    assert ratings[0]["username"] == "multiple_ratings_user3"
    assert ratings[0]["points"] == 3
    assert ratings[0]["description"] == "test description3"


def test_create_rating_by_user_that_already_rated_the_app(test_client):
    # create user
    username = 'sample_rater'
    logintoken = '41ffda91-1eb2-47dc-8e30-189ac6eb3050'
    createTestUser(test_client, username, logintoken)
    # the test
    # create rating
    response = test_client.post('/ratings/sample.app3/add', json={
        'username': username,
        'logintoken': logintoken,
        'points': 5,
        'description': "an essential app for everyone"
    })
    assert response.status_code == 201
    assert response.get_json() == dict(success=True)
    # try to add another rating to the app from the same user
    response = test_client.post('/ratings/sample.app3/add', json={
        'username': username,
        'logintoken': logintoken,
        'points': 5,
        'description': "you need to download this"
    })
    assert response.status_code == 409
    assert response.get_json() == dict(
        success=False, error="you already posted a review for this app")
