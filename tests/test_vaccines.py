from flask_jwt_extended import create_access_token
import pytest
from app.core.extensions import db
from app.auth.models.user import User


# Fixture
@pytest.fixture
def pet_id(client, auth_token):
    res = client.post(
        "/api/v1/pets",
        json={"name": "Sandy", "species": "Perro"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    return res.get_json()["mascota"]["id"]


# Pruebas unitarias
def test_get_vaccines_sin_token(client, pet_id):
    """Sin token debe devolver 401"""
    res = client.get(f"/api/v1/pets/{pet_id}/vaccines")
    print(f"\nRespuesta sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401


def test_crear_vacuna_datos_incompletos(client, auth_token, pet_id):
    """Sin datos obligatorios debe devolver 422"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"date_applied": "2024-08-02"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError data incompleta: {res.status_code} - {res.get_json()}")
    assert res.status_code == 400


def test_crear_vacuna_mascota_inexistente(client, auth_token):
    """ID que no existe debe devolver 404"""
    res = client.post(
        "/api/v1/pets/785/vaccines",
        json={"name": "Rabia", "date_applied": "2024-08-02"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError mascota no encontrada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


# Pruebas de integración
def test_get_vaccines_con_token(client, auth_token, pet_id):
    """Con token válido debe devolver lista vacía"""
    res = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nLista de vacunas: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert len(res.get_json()["vacunas"]) == 0


def test_crear_vacuna_exitoso(client, auth_token, pet_id):
    """Crear vacuna con datos válidos"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Rabia", "vet": "Pedro Perez", "date_applied": "2024-08-02"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nVacuna creada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201
    data = res.get_json()
    assert isinstance(data["vacuna"]["id"], int)
    assert data["vacuna"]["name"] == "Rabia"
    assert data["vacuna"]["date_applied"] == "2024-08-02"


def test_actualizar_vacuna(client, auth_token, pet_id):
    """Crear y luego actualizar una vacuna"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={
            "name": "Parvovirus vacuna prueba",
            "vet": "Pedro Perez",
            "date_applied": "2024-08-02",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vacuna_id = res.get_json()["vacuna"]["id"]
    print(f"\nVacuna creada para actualizar: {res.status_code} - id={vacuna_id}")

    res = client.put(
        f"/api/v1/vaccines/{vacuna_id}",
        json={"name": "Parvovirus"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"Vacuna actualizada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()["vacuna"]["name"] == "Parvovirus"


def test_eliminar_vacuna(client, auth_token, pet_id):
    """Crear y luego eliminar una vacuna"""
    res_post = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={
            "name": "Rabia vacuna para eliminar",
            "vet": "Pedro Perez",
            "date_applied": "2024-08-02",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vacuna_id = res_post.get_json()["vacuna"]["id"]
    print(f"\nVacuna creada para eliminar: {res_post.status_code} - id={vacuna_id}")

    res_del = client.delete(
        f"/api/v1/vaccines/{vacuna_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"Vacuna eliminada: {res_del.status_code} - {res_del.get_json()}")
    assert res_del.status_code == 200


def test_obtener_vacuna_id(client, auth_token, pet_id):
    """Obtener detalle de una vacuna"""
    res_post = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Rabia", "vet": "Juan josé", "date_applied": "2024-08-02"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vacuna_id = res_post.get_json()["vacuna"]["id"]

    res = client.get(
        f"/api/v1/vaccines/{vacuna_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert res.status_code == 200
    assert res.get_json()["vacuna"]["name"] == "Rabia"


def test_acceso_con_rol_admin(client, app, pet_id):
    """Un admin no puede acceder a vaccines, debe devolver 403"""

    with app.app_context():
        admin = User(name="Admin", email="admin@petcare.com", role="admin")
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()

        from flask_jwt_extended import create_access_token

        with app.test_request_context():
            token = create_access_token(
                identity=str(admin.id), additional_claims={"role": "admin"}
            )

    res = client.get(
        f"/api/v1/pets/{pet_id}/vaccines", headers={"Authorization": f"Bearer {token}"}
    )
    print(f"\nAcceso con rol admin: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_get_vaccines_mascota_ajena(client, app, pet_id):
    """Un usuario no puede acceder a ver vacunas de las mascotas de otros usuarios"""

    with app.app_context():
        userNoDueño = User(name="user 1", email="user1@petcare.com")
        userNoDueño.set_password("123456")
        db.session.add(userNoDueño)
        db.session.commit()

        with app.test_request_context():
            token_userNoDueño = create_access_token(identity=str(userNoDueño.id))

        # probamos acceder a vacunas de Sandy, creada anteriormente.

        res = client.get(
            f"/api/v1/pets/{pet_id}/vaccines",
            headers={"Authorization": f"Bearer {token_userNoDueño}"},
        )

        assert res.status_code == 404
