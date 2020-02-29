import os
import tempfile
from price_scraper import app

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
    rv = client.get('/assets/summary')
    assert b'This is your portfolio:' in rv.data


def test_round_quantity():
    assert round(5.3333) == 5.333


def test_response(client):
    response = client.get("/users/register")
    assert response.status_code == 200

def test_error(client):
    response = client.get("/thereisnotthatroute")
    assert response.status_code == 404
