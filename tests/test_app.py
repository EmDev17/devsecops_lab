import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.app import app, db

TEST_PASSWORD = os.environ.get('TEST_PASSWORD', 'test_password')
TEST_USERNAME = os.environ.get('TEST_USERNAME', 'testuser')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_login_exists(client):
    response = client.post('/login', json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
    assert response.status_code in [200, 401]

def test_sql_injection_login(client):
    response = client.post('/login', json={'username': "' OR '1'='1", 'password': TEST_PASSWORD})
    assert response.status_code == 401

def test_add_note(client):
    response = client.post('/notes', json={'user_id': 1, 'content': 'test note'})
    assert response.status_code == 200

def test_get_notes(client):
    response = client.get('/notes/1')
    assert response.status_code == 200

def test_users_endpoint_does_not_expose_passwords(client):
    response = client.get('/users')
    data = response.get_json()
    for user in data.get('users', []):
        assert 'password' not in user

def test_ping_endpoint_exists(client):
    response = client.get('/ping?host=localhost')
    assert response.status_code == 200

def test_debug_mode_disabled(client):
    assert app.config.get('DEBUG') == False
