from src import create_app
import pytest
import sys
import os
from tempfile import mkdtemp


@pytest.fixture(scope='module')
def test_client():
    database = mkdtemp() + "test.db"
    print(database)

    flask_app = create_app(database)

    testing_client = flask_app.test_client()

    with flask_app.app_context():
        yield testing_client  # this is where the testing happens!
