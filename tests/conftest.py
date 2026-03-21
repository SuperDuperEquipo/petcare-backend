import pytest
import os
import logging

os.environ['FLASK_ENV'] = 'testing'

logging.basicConfig(level=logging.DEBUG) 

from app import create_app
from app.core.extensions import db

@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    res = client.post('/api/v1/auth/register', json={
        "name": "Test User",
        "email": "test@petcare.com",
        "password": "123456"
    })
    return res.get_json()['access_token']