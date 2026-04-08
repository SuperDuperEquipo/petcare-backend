import pytest
import os
import logging

os.environ["FLASK_ENV"] = "testing"

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
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": "test@petcare.com", "password": "123456"},
    )
    return res.get_json()["access_token"]


@pytest.fixture
def pet_id(client, auth_token):
    res = client.post(
        "/api/v1/pets",
        json={"name": "Sandy", "species": "Perro"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return res.get_json()["mascota"]["id"]


@pytest.fixture
def admin_token(client, app):
    from app.auth.models.user import User

    with app.app_context():
        admin = User(name="Admin", email="admin@petcare.com", role="admin")
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()

        from flask_jwt_extended import create_access_token
        with app.test_request_context():
            token = create_access_token(
                identity=str(admin.id),
                additional_claims={"role": "admin"}
            )
    return token


@pytest.fixture
def appointment_id(client, auth_token, pet_id):
    res = client.post(
        "/api/v1/appointments",
        json={
            "title": "Consulta general",
            "date": "2026-04-01",
            "time": "10:00:00",
            "type": "Consulta",
            "pet_id": pet_id
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return res.get_json()["cita"]["id"]


@pytest.fixture
def usuario_registrado(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": "test@petcare.com", "password": "password123"},
    )
    data = res.get_json()
    return {"user": data["user"], "token": data["access_token"], "password": "password123"}


@pytest.fixture
def usuario_admin(client, app):
    from app.auth.models.user import User

    with app.app_context():
        admin = User(name="Admin User", email="admin@petcare.com", role="admin")
        admin.set_password("adminpass123")
        db.session.add(admin)
        db.session.commit()

        from flask_jwt_extended import create_access_token
        with app.test_request_context():
            token = create_access_token(
                identity=str(admin.id),
                additional_claims={"role": "admin"}
            )
    return {"user": {"email": "admin@petcare.com"}, "token": token}