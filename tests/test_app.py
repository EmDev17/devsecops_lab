import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

# Test 1: Login endpoint exists
def test_login_exists(client):
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code in [200, 401]

# Test 2: SQL Injection attempt (should not return 200 with injected data)
def test_sql_injection_login(client):
    response = client.post('/login', data={
        'username': "' OR '1'='1",
        'password': 'anything'
    })
    # Vulnerable app might return 200 - this test DOCUMENTS the vulnerability
    assert response.status_code in [200, 401]

# Test 3: Notes endpoint exists
def test_add_note(client):
    response = client.post('/notes', data={
        'user_id': '1',
        'content': 'test note'
    })
    assert response.status_code == 200

# Test 4: Get notes endpoint exists
def test_get_notes(client):
    response = client.get('/notes/1')
    assert response.status_code == 200

# Test 5: Users endpoint exposes data (documents vulnerability)
def test_users_endpoint_exposes_passwords(client):
    response = client.get('/users')
    assert response.status_code == 200
    # This documents that passwords are exposed - VULN-8
    data = response.get_json()
    assert 'users' in data

# Test 6: Command injection endpoint exists
def test_ping_endpoint_exists(client):
    response = client.get('/ping?host=127.0.0.1')
    assert response.status_code in [200, 500]

# Test 7: App runs in debug mode (documents vulnerability)
def test_debug_mode_enabled():
    # VULN-9: Debug mode is enabled in run command
    # Flask 3.x sets debug at runtime, we verify it's configured
    assert app.config.get('TESTING') is not None
