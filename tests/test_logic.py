from app import app
import pytest
from models import User, Application
from passlib.hash import sha256_crypt

@pytest.fixture
def client():
    return app.test_client()

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