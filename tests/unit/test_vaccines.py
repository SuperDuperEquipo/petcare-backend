from flask_jwt_extended import create_access_token
import pytest
from app.core.extensions import db
from app.auth.models.user import User

def test_get_vaccines_sin_token(client, pet_id):
    """Sin token debe devolver 401"""
    res = client.get(f"/api/v1/pets/{pet_id}/vaccines")
    print(f"\nRespuesta sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401

def test_crear_vacuna_campos_vacios(client, auth_token, pet_id):
    """Campos obligatorios vacíos deben devolver 422"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "", "vet": "", "date_applied": ""},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nCampos vacíos: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422

def test_eliminar_vacuna_sin_token(client):
    """DELETE sin token debe devolver 401"""
    res = client.delete("/api/v1/vaccines/785")
    print(f"\nDELETE sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401

def test_actualizar_vacuna_sin_token(client):
    """PUT sin token debe devolver 401"""
    res = client.put(
        "/api/v1/vaccines/785",
        json={"name": "Rabia"},
    )
    print(f"\nPUT sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401

def test_crear_vacuna_datos_incompletos(client, auth_token, pet_id):
    """Sin datos obligatorios debe devolver 422"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"date_applied": "2024-08-02"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError data incompleta: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422


def test_crear_vacuna_mascota_inexistente(client, auth_token):
    """ID que no existe debe devolver 404"""
    res = client.post(
        "/api/v1/pets/785/vaccines",
        json={"name": "Rabia", "date_applied": "2024-08-02"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError mascota no encontrada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_eliminar_vacuna_inexistente(client, auth_token):
    """Eliminar un ID que no existe, debe devolver 404"""
    res = client.delete(
        "/api/v1/vaccines/785", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nEliminar vacuna inexistente: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_actualizar_vacuna_inexistente(client, auth_token):
    """Actualizar un ID que no existe, debe devolver 404"""
    res = client.put(
        "/api/v1/vaccines/785",
        json={"name": "Rabia"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nActualizar vacuna inexistente: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_token_expirado(client, app, pet_id):
    """Token vencido, debe devolver 401"""
    from flask_jwt_extended import create_access_token
    from datetime import timedelta

    with app.app_context():
        with app.test_request_context():
            token_expirado = create_access_token(
                identity="1", expires_delta=timedelta(seconds=-1)
            )
    res = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {token_expirado}"},
    )
    print(f"\nError token expirado: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401


def test_crear_vacuna_body_no_json(client, auth_token, pet_id):
    """Body que no es JSON, debe devolver 400"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        data="no es un JSON",
        content_type="text/plain",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError debe ser un JSON: {res.status_code} - {res.get_json()}")
    assert res.status_code == 400



