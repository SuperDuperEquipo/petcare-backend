def test_get_pets_sin_token(client):
    """Sin token debe devolver 401"""
    res = client.get("/api/v1/pets")
    print(f"\nRespuesta sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401


def test_crear_mascota_sin_nombre(client, auth_token):
    """Sin nombre debe devolver 422"""
    res = client.post(
        "/api/v1/pets",
        json={"species": "Perro"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError sin nombre: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422


def test_crear_mascota_sin_especie(client, auth_token):
    """Sin especie debe devolver 422"""
    res = client.post(
        "/api/v1/pets",
        json={"name": "Firulais"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError sin especie: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422


def test_obtener_mascota_inexistente(client, auth_token):
    """ID que no existe debe devolver 404"""
    res = client.get(
        "/api/v1/pets/999", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nMascota no encontrada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_token_expirado(client, app):
    """Token vencido, debe devolver 401"""
    from flask_jwt_extended import create_access_token
    from datetime import timedelta

    with app.app_context():
        with app.test_request_context():
            token_expirado = create_access_token(
                identity="1", expires_delta=timedelta(seconds=-1)
            )

    res = client.get(
        "/api/v1/pets", headers={"Authorization": f"Bearer {token_expirado}"}
    )
    print(f"\nError token expirado: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401


def test_crear_mascota_body_no_json(client, auth_token):
    """Body que no es JSON, debe devolver 400"""
    res = client.post(
        "/api/v1/pets",
        data="no es un JSON",
        content_type="text/plain",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError debe ser un JSON: {res.status_code} - {res.get_json()}")
    assert res.status_code == 400


def test_crear_mascota_con_todos_los_campos(client, auth_token):
    """Crear mascota con todos los campos opcionales incluidos, debe devolver 201"""
    res = client.post(
        "/api/v1/pets",
        json={
            "name": "Rocky",
            "species": "Perro",
            "breed": "Labrador",
            "birth_date": "2022-05-10",
            "weight": 12.5,
            "photo_url": "http://example.com/rocky.jpg",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nMascota con todos los campos: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201
    data = res.get_json()
    assert data["mascota"]["raza"] == "Labrador"
    assert data["mascota"]["peso"] == 12.5
