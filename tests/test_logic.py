from app import create_app
import pytest
from flask import Flask, current_app
from flask.testing import FlaskClient
from models import User, Application, db
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from passlib.hash import sha256_crypt

@pytest.fixture(scope='session')
def app():
    app = create_app(config="config.DevelopmentConfig")
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

# @pytest.fixture(scope='module')
# def flask_app():
#     app = create_app()
#     with app.app_context():
#         yield app

# @pytest.fixture(scope='module')
# def client(flask_app):
#     app = flask_app
#     ctx = flask_app.test_request_context()
#     ctx.push()
#     app.test_client_class = FlaskClient
#     return app.test_client()

def capital_case(x):
    if not isinstance(x, str):
        raise TypeError('Please provide a string argument')
    return x.capitalize()

def test_capital_case():
    assert capital_case('apple') == 'Apple'
    
def test_capital_case2():
    assert capital_case('london') == 'London'

def test_raises_exception_on_non_string_arguments():
    with pytest.raises(TypeError):
        capital_case(9)

# @pytest.fixture
# def login(client):
#     user = User.query.filter_by(username='thor.odinson').first()
#     login_user(user)

# @pytest.mark.usefixtures("login")
# def test_user_login(client):
#     with app.test_client:
#         resp = client.get("/")
#         assert resp.status_code == 200

# def test_db(client):
    # resp = client.get("/login")
    # assert resp.status_code == 200
    # user = User.query.filter_by(username='thor.odinson').first()
    # assert user.email == 'thor.odinson@email.com'
    # client.post('/login', data=dict(username='thor.odinson', password='computer'))
    # res = client.get('/')
    # assert res.status_code == 200


# Check that the login route returns the appropriate status code
def test_home(client):
    resp = client.get("/login")

    assert resp.status_code == 200
    assert b"Product Owners Login" in resp.data

# Check the creation of a user given the User data model
def test_user_model():
    user = User(first_name='TestF', last_name = 'TestL', username='testf.testl', email = 'test.test@email.com', password = 'abc123', is_admin=0)
    assert user.email == 'test.test@email.com'
    assert user.is_admin == 0

# Check creation of an application given the Application data model
def test_application_model():
    testApp = Application(name='Test', description='Test application')
    assert testApp.description == 'Test application'

# Check appending of users to applications given the Application and User data models
def test_table_relationship():
    testUser = User(first_name='TestF', last_name = 'TestL', username='testf.testl', email = 'test.test@email.com', password = 'abc123', is_admin=0)
    testUser2 = User(first_name='TestF2', last_name = 'TestL2', username='testf2.testl2', email = 'test2.test@email.com', password = 'abc246', is_admin=0)
    testApp = Application(name='Test', description='Test application')
    testApp.users.append(testUser)
    testApp.users.append(testUser2)

    assert len(list(testApp.users)) == 2

# Check the hashing of passwords
def test_password_hashing():
    encryptedPassword = sha256_crypt.hash("testPassword")
    assert encryptedPassword != "testPassword"

# Check the verification of hashed passwords
def test_password_verification():
    encryptedPassword = sha256_crypt.hash("testPassword")
    assert sha256_crypt.verify("testPassword", encryptedPassword)

# # Check the login functionality works
# def test_login():
#     with app.app_context():
#         user = User.query.filter_by(username='thor.odinson').first()
#         # assert user.email == 'thor.odinson2@email.com'
#         login_user(user)
#         # client.post('/login', data=dict(username='thor.odinson', password='keyboard'))
#         res = app.get('/')
#         assert res.status_code == 200