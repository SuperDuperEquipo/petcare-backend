def test_get_pets_con_token(client, auth_token):
    """Con token válido debe devolver lista vacía"""
    res = client.get("/api/v1/pets", headers={"Authorization": f"Bearer {auth_token}"})
    print(f"\nLista de mascotas: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()["total"] == 0


def test_crear_mascota_exitoso(client, auth_token):
    """Crear mascota con datos válidos"""
    res = client.post(
        "/api/v1/pets",
        json={"name": "Firulais", "species": "Perro"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nMascota creada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201
    assert res.get_json()["mascota"]["nombre"] == "Firulais"


def test_actualizar_mascota(client, auth_token):
    """Crear y luego actualizar una mascota"""
    res = client.post(
        "/api/v1/pets",
        json={"name": "Luna", "species": "Gato"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    pet_id = res.get_json()["mascota"]["id"]
    print(f"\nMascota creada para actualizar: {res.status_code} - id={pet_id}")

    res = client.put(
        f"/api/v1/pets/{pet_id}",
        json={"name": "Luna Updated"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"Mascota actualizada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()["mascota"]["nombre"] == "Luna Updated"


def test_eliminar_mascota(client, auth_token):
    """Crear y luego eliminar una mascota"""
    res = client.post(
        "/api/v1/pets",
        json={"name": "Rex", "species": "Perro"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    pet_id = res.get_json()["mascota"]["id"]
    print(f"\nMascota creada para eliminar: {res.status_code} - id={pet_id}")

    res = client.delete(
        f"/api/v1/pets/{pet_id}", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"Mascota eliminada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_acceso_con_rol_admin(client, app):
    """Un admin no puede acceder a pets, debe devolver 403"""
    from app.core.extensions import db
    from app.auth.models.user import User

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

    res = client.get("/api/v1/pets", headers={"Authorization": f"Bearer {token}"})
    print(f"\nAcceso con rol admin: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403


def test_eliminar_mascota_inexistente(client, auth_token):
    """Eliminar un ID que no existe, debe devolver 404"""
    res = client.delete(
        "/api/v1/pets/999", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nEliminar mascota inexistente: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_actualizar_mascota_inexistente(client, auth_token):
    """Actualizar un ID que no existe, debe devolver 404"""
    res = client.put(
        "/api/v1/pets/999",
        json={"name": "Robin"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nActualizar mascota inexistente: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_crear_mascota_y_agregar_vacuna(client, auth_token, pet_id):
    """Crear mascota y agregar vacuna, debe devolver 201 y aparecer en el historial"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Rabia", "vet": "Dr. López", "date_applied": "2026-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nVacuna agregada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201

    res_lista = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nHistorial de vacunas: {res_lista.status_code} - {res_lista.get_json()}")
    assert res_lista.status_code == 200
    vacunas = res_lista.get_json()["vacunas"]
    assert len(vacunas) == 1
    assert vacunas[0]["name"] == "Rabia"
