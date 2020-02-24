import os
import tempfile
from Price_scraper import app, Price_scraper

import pytest



@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        # with app.app_context():
            #Price_scraper.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_index(client):
    rv = client.get('/summary')
    assert b'No entries here so far' in rv.data
