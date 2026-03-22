<<<<<<< Updated upstream
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
=======
import os
import pytest
from sqlalchemy.pool import StaticPool

os.environ["FLASK_ENV"] = "testing"

from app import create_app
from app.core.extensions import db as _db, revoked_tokens


@pytest.fixture(scope="session")
def app():
    """
    Crea la app una sola vez para toda la sesión de tests.
    StaticPool hace que todas las conexiones compartan la misma BD
    SQLite en memoria (sin él, cada conexión nueva recibiría una BD vacía).
    """
    application = create_app()
    application.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }

    ctx = application.app_context()
    ctx.push()
    _db.create_all()

    yield application

    _db.drop_all()
    ctx.pop()


@pytest.fixture()
def client(app):
    """Cliente HTTP para hacer peticiones a la API en cada test."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db():
    """Limpia todas las tablas y tokens revocados entre tests."""
    yield
    # Si el test dejó la sesión con un error pendiente, hacemos rollback primero
    _db.session.rollback()
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()
    revoked_tokens.clear()


@pytest.fixture()
def usuario_registrado(client):
    """Registra un usuario de prueba y devuelve sus datos + token."""
    payload = {
        "name": "Test User",
        "email": "test@petcare.com",
        "password": "password123",
    }
    resp = client.post("/api/v1/auth/register", json=payload)
    data = resp.get_json()
    return {"user": data["user"], "token": data["access_token"], "password": payload["password"]}


@pytest.fixture()
def usuario_admin(client):
    """Crea un usuario admin directamente en la BD y devuelve sus datos + token."""
    from app.auth.models.user import User

    admin = User(name="Admin User", email="admin@petcare.com", role="admin")
    admin.set_password("adminpass123")
    _db.session.add(admin)
    _db.session.commit()
    user_dict = admin.to_dict()

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@petcare.com", "password": "adminpass123"},
    )
    token = resp.get_json()["access_token"]
    return {"user": user_dict, "token": token}
>>>>>>> Stashed changes
