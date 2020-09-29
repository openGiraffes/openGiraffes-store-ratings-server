
def test_download_counter_empty(test_client):
    response = test_client.get('/download_counter')
    assert response.status_code == 200
    assert response.get_json() == dict()


def test_download_counter_add_and_retrieve(test_client):
    response = test_client.get('/download_counter')
    assert response.status_code == 200
    assert response.get_json() == dict()

    response = test_client.get('/download_counter/count/sampleapp')
    assert response.status_code == 200
    assert response.data == b"OK"

    response = test_client.get('/download_counter')
    assert response.status_code == 200
    assert response.get_json() == dict(sampleapp=1)

    test_client.get('/download_counter/count/sampleapp')
    test_client.get('/download_counter/count/sampleapp')
    test_client.get('/download_counter/count/sampleapp')
    response = test_client.get('/download_counter')
    assert response.get_json() == dict(sampleapp=4)

    test_client.get('/download_counter/count/app_sample')
    response = test_client.get('/download_counter')
    assert response.get_json() == dict(sampleapp=4, app_sample=1)
