from price_scraper import app, db
from price_scraper.models import User
from price_scraper.assets.functions import round_quantity
from price_scraper.users.forms import RegistrationForm, LoginForm
import pytest

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    db.create_all()
    with app.test_client() as client:
        yield client
    db.drop_all()


def test_index(client):
    rv = client.get('/assets/summary')
    assert b'This is your portfolio:' in rv.data


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


# def test_login_user(client):
#     """Testing login user to DB"""
#     post_register = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
#                                           'password':'one','password_confirm':'one'})
#     post_login = client.post('/users/login', data={'email':'one@one.com', 'password':'one'})
#     assert b'Welcome to our Price Scraper site!' in post_login.data


def test_validate_email(client):
    """Testing email validator"""
    post = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                          'password':'one','password_confirm':'one'})
    post = client.post('/users/register', data={'email':'one@one.com', 'username':'one',
                                          'password':'one','password_confirm':'one'})
    assert b'Email you have chosen is already taken!' in post.data
    assert b'Username you have chosen is already taken!' in post.data

