from price_scraper import app, db, mail
from price_scraper.models import User
from price_scraper.assets.functions import round_quantity
from price_scraper.users.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import pytest
import responses
import requests

from unittest import mock



@pytest.fixture()
def db_fixture():
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture
def client(db_fixture):
    with app.test_client() as client:
        yield client


@pytest.fixture
def user(db_fixture):
    user = User(email="one@one.com",
                username="one",
                password=generate_password_hash("one"),
                confirmed=False)

    db.session.add(user)
    db.session.commit()


def test_index(client):
    rv = client.get('/')
    assert b'Current assets prices:' in rv.data


def test_round_quantity():
    assert round_quantity(2.222) == 2.222
    assert round_quantity(0) == 0.0


def test_response(client):
    response = client.get("/users/register")
    assert response.status_code == 200, "That route exists"


def test_error(client):
    response = client.get("/thereisnotthatroute")
    assert response.status_code == 404, "That route doesn't exist"


def test_register_form(client):
    """Testing register form"""
    with app.test_request_context('/', method='POST', data={'email':'one@one.com', 'username':'one',
                                          'password':'one','password_confirm':'one'}):
        f = RegistrationForm()
        assert f.validate() is True , f.errors


def test_login_form(client):
    """Testing login form"""
    with app.test_request_context('/', method='POST', data={'email':'one@one.com', 'password':'one'}):
        f = LoginForm()
        assert f.validate() is True , f.errors


def test_register_user(client):
    """Testing posting user to DB"""
    with mail.record_messages() as outbox:
        post = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                              'password':'one','password_confirm':'one'})
        user1 = User.query.filter_by(email='one@one.com',username='one').first()
        assert user1.email == 'one@one.com'
        assert len(outbox) == 1
        assert outbox[0].subject == "Please confirm your email"


def test_login_user(client):
    """Testing login user to DB"""
    with mock.patch('price_scraper.assets.views.check_price_btc',return_value = 3):
        with mock.patch('price_scraper.assets.views.check_price_xrp',return_value = 3):
            with mock.patch('price_scraper.assets.views.check_price_xlm',return_value = 3):
                with mock.patch('price_scraper.assets.views.check_price_gld',return_value = 3):
                    with mail.record_messages() as outbox:
                        post_register = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                                              'password':'one','password_confirm':'one'})
                        post_login = client.post('/users/login', data={'email':'one@one.com', 'password':'one',}, follow_redirects=True)
                        assert b'Welcome to our Price Scraper site!' in post_login.data


def test_validate_email(client):
    """Testing email validator"""

    with mail.record_messages() as outbox:
        post = client.post('/users/register', data={'email': 'one@one.com', 'username': 'one',
                                                    'password': 'one', 'password_confirm': 'one'})
        post = client.post('/users/register', data={'email': 'one@one.com', 'username': 'one',
                                                    'password': 'one', 'password_confirm': 'one'})

        assert b'Email you have chosen is already taken!' in post.data
        assert b'Username you have chosen is already taken!' in post.data

@responses.activate
def test_add_asset(user, client):
    responses.add(responses.GET, 'http://package/',
                  json={"BTC":1.0,"XRP":1.0,"XLM":1.0,"GLD":1.0,"USD":1.0})
    resp = requests.get('http://package/')

    post_login = client.post('/users/login', data={'email': 'one@one.com', 'password': 'one', })
    post_asset = client.post('/add_asset', data={'quantity_btc':'14545', 'quantity_xrp':'2',
                                              'quantity_xlm':'3','quantity_gld':'4'},follow_redirects=True)

    assert b'14545' in post_asset.data
    assert resp.json() == {"BTC":1.0,"XRP":1.0,"XLM":1.0,"GLD":1.0,"USD":1.0}


def test_crypting_decrypting_password(client):
    """Testing hashing passwords"""
    with mail.record_messages() as outbox:
        post = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                              'password':'one','password_confirm':'one'})
        user1 = User.query.filter_by(email='one@one.com',username='one').first()
        assert check_password_hash(user1.password, 'one')





