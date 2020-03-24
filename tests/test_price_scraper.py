from price_scraper import app, db
from price_scraper.models import User
from price_scraper.assets.functions import round_quantity
from price_scraper.users.forms import RegistrationForm, LoginForm
import pytest
from unittest import mock

@pytest.fixture()
def db_fixture():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
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
                password="one")

    db.session.add(user)
    db.session.commit()


def test_index(client):
    rv = client.get('/')
    assert b'Actual assets prices:' in rv.data


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
    post = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                          'password':'one','password_confirm':'one'})
    user1 = User.query.filter_by(email='one@one.com',username='one',password='one').first()
    assert user1.email == 'one@one.com'


def test_login_user(client):
    """Testing login user to DB"""
    with mock.patch('price_scraper.assets.views.check_price_btc',return_value = 3):
        with mock.patch('price_scraper.assets.views.check_price_xrp',return_value = 3):
            with mock.patch('price_scraper.assets.views.check_price_xlm',return_value = 3):
                with mock.patch('price_scraper.assets.views.check_price_gld',return_value = 3):
                    post_register = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                                          'password':'one','password_confirm':'one'})
                    post_login = client.post('/users/login', data={'email':'one@one.com', 'password':'one',}, follow_redirects=True)
                    assert b'Welcome to our Price Scraper site!' in post_login.data


def test_validate_email(client):
    """Testing email validator"""
    post = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                          'password':'one','password_confirm':'one'})
    post = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                          'password':'one','password_confirm':'one'})
    assert b'Email you have chosen is already taken!' in post.data
    assert b'Username you have chosen is already taken!' in post.data


def test_add_asset(user,client):
    post_login = client.post('/users/login', data={'email': 'one@one.com', 'password': 'one', })
    post_asset = client.post('/add_asset', data={'quantity_btc':'14545', 'quantity_xrp':'2',
                                          'quantity_xlm':'3','quantity_gld':'4'},follow_redirects=True)
    assert b'14545' in post_asset.data





