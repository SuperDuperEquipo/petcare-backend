
def test_get_vaccines_con_token(client, auth_token, pet_id):
    """Con token válido debe devolver lista vacía"""
    res = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nLista de vacunas: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert len(res.get_json()["vacunas"]) == 0

def test_actualizar_vacuna(client, auth_token, pet_id):
    """Crear y actualizar nombre de vacuna"""
    res_create = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Moquillo Original", "vet": "Dr. Ruiz", "date_applied": "2025-01-15"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vaccine_id = res_create.get_json()["vacuna"]["id"]

    res = client.put(
        f"/api/v1/vaccines/{vaccine_id}",
        json={"name": "Moquillo Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nActualizar vacuna: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()["vacuna"]["name"] == "Moquillo Actualizado"

def test_actualizar_next_dose(client, auth_token, pet_id):
    """Actualizar next_dose de una vacuna existente"""
    res_create = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Hepatitis", "vet": "Dr. Ruiz", "date_applied": "2025-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vaccine_id = res_create.get_json()["vacuna"]["id"]

    res = client.put(
        f"/api/v1/vaccines/{vaccine_id}",
        json={"next_dose": "2026-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert res.status_code == 200
    assert res.get_json()["vacuna"]["next_dose"] == "2026-01-01"

def test_eliminar_vacuna(client, auth_token, pet_id):
    """Crear y eliminar vacuna,luego GET devuelve 404"""
    res_create = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Triple Canina", "vet": "Dr. Mora", "date_applied": "2025-06-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vaccine_id = res_create.get_json()["vacuna"]["id"]

    res_del = client.delete(
        f"/api/v1/vaccines/{vaccine_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nEliminar vacuna: {res_del.status_code} - {res_del.get_json()}")
    assert res_del.status_code == 200

    res_get = client.get(
        f"/api/v1/vaccines/{vaccine_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert res_get.status_code == 404

def test_acceso_con_rol_admin(client, app, pet_id):
    """Un admin no puede acceder a vaccines, debe devolver 403"""
    from flask_jwt_extended import create_access_token
    from app.auth.models.user import User
    from app.core.extensions import db
 
    with app.app_context():
        admin = User(name="Admin", email="admin@petcare.com", role="admin")
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()
 
        with app.test_request_context():
            token = create_access_token(
                identity=str(admin.id), additional_claims={"role": "admin"}
            )
 
    res = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {token}"},
    )
    print(f"\nAcceso con rol admin: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403

def test_get_vaccines_mascota_ajena(client, app, pet_id):
    """Un usuario no puede ver vacunas de mascotas de otros usuarios"""
    from flask_jwt_extended import create_access_token
    from app.auth.models.user import User
    from app.core.extensions import db
 
    with app.app_context():
        userNoDueno = User(name="user 1", email="user1@petcare.com")
        userNoDueno.set_password("123456")
        db.session.add(userNoDueno)
        db.session.commit()
 
        with app.test_request_context():
            token_userNoDueno = create_access_token(
                identity=str(userNoDueno.id), additional_claims={"role": "user"}
            )
 
    res = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {token_userNoDueno}"},
    )
    print(f"\nMascota ajena: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404

def test_crear_mascota_y_agregar_vacuna_historial(client, auth_token):
    """Crear mascota y agregar vacuna al historial"""
    res_pet = client.post(
        "/api/v1/pets",
        json={"name": "Bolt", "species": "Perro", "breed": "Dálmata"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"Crear mascota: {res_pet.status_code} - {res_pet.get_json()}")
    assert res_pet.status_code == 201
    pet_id = res_pet.get_json()["mascota"]["id"]

    res_vac = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Rabia", "vet": "Dr. Juan", "date_applied": "2026-01-10"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"Agregar vacuna: {res_vac.status_code} - {res_vac.get_json()}")
    assert res_vac.status_code == 201

    res_list = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"Historial: {res_list.status_code} - {res_list.get_json()}")
    assert res_list.status_code == 200
    vacunas = res_list.get_json()["vacunas"]
    assert len(vacunas) == 1
    assert vacunas[0]["name"] == "Rabia"
    assert vacunas[0]["pet_id"] == pet_id

def test_multiples_vacunas_en_historial(client, auth_token):
    """Agregar 3 vacunas al historial"""
    res_pet = client.post(
        "/api/v1/pets",
        json={"name": "Max", "species": "Perro"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    pet_id = res_pet.get_json()["mascota"]["id"]

    vacunas_a_crear = [
        {"name": "Rabia", "vet": "Dr. Pedro", "date_applied": "2025-01-01"},
        {"name": "Parvovirus", "vet": "Dr. Juan", "date_applied": "2025-03-01"},
        {"name": "Moquillo", "vet": "Dr. Carlos", "date_applied": "2025-06-01"},
    ]
    ids_creados = []
    for datos in vacunas_a_crear:
        r = client.post(
            f"/api/v1/pets/{pet_id}/vaccines",
            json=datos,
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert r.status_code == 201
        ids_creados.append(r.get_json()["vacuna"]["id"])

    res_list = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nHistorial de vacunas: {res_list.status_code} - {res_list.get_json()}")
    assert res_list.status_code == 200
    vacunas = res_list.get_json()["vacunas"]
    assert len(vacunas) == 3

    nombres_en_historial = {v["name"] for v in vacunas}
    assert nombres_en_historial == {"Rabia", "Parvovirus", "Moquillo"}

    