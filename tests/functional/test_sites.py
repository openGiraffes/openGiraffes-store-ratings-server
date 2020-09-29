def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Simple rating and download counter backend" in response.data


def test_not_found(test_client):
    response = test_client.get('/unreal/path')
    assert response.status_code == 404
    assert response.get_json() == dict(error='404 Not Found')
