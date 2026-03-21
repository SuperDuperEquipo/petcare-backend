# Pruebas unitarias
def test_get_pets_sin_token(client):
    """Sin token debe devolver 401"""
    res = client.get('/api/v1/pets')
    print(f"\nRespuesta sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401

def test_crear_mascota_sin_nombre(client, auth_token):
    """Sin nombre debe devolver 422"""
    res = client.post('/api/v1/pets', json={
        "species": "Perro"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    print(f"\nError sin nombre: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422

def test_crear_mascota_sin_especie(client, auth_token):
    """Sin especie debe devolver 422"""
    res = client.post('/api/v1/pets', json={
        "name": "Firulais"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    print(f"\nError sin especie: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422

def test_obtener_mascota_inexistente(client, auth_token):
    """ID que no existe debe devolver 404"""
    res = client.get('/api/v1/pets/999', headers={
        "Authorization": f"Bearer {auth_token}"
    })
    print(f"\nMascota no encontrada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404

# Pruebas de integración
def test_get_pets_con_token(client, auth_token):
    """Con token válido debe devolver lista vacía"""
    res = client.get('/api/v1/pets', headers={
        "Authorization": f"Bearer {auth_token}"
    })
    print(f"\nLista de mascotas: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()['total'] == 0

def test_crear_mascota_exitoso(client, auth_token):
    """Crear mascota con datos válidos"""
    res = client.post('/api/v1/pets', json={
        "name": "Firulais",
        "species": "Perro"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    print(f"\nMascota creada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201
    assert res.get_json()['mascota']['nombre'] == 'Firulais'

def test_actualizar_mascota(client, auth_token):
    """Crear y luego actualizar una mascota"""
    res = client.post('/api/v1/pets', json={
        "name": "Luna", "species": "Gato"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    pet_id = res.get_json()['mascota']['id']
    print(f"\nMascota creada para actualizar: {res.status_code} - id={pet_id}")

    res = client.put(f'/api/v1/pets/{pet_id}', json={
        "name": "Luna Updated"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    print(f"Mascota actualizada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()['mascota']['nombre'] == 'Luna Updated'

def test_eliminar_mascota(client, auth_token):
    """Crear y luego eliminar una mascota"""
    res = client.post('/api/v1/pets', json={
        "name": "Rex", "species": "Perro"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    pet_id = res.get_json()['mascota']['id']
    print(f"\nMascota creada para eliminar: {res.status_code} - id={pet_id}")

    res = client.delete(f'/api/v1/pets/{pet_id}', headers={
        "Authorization": f"Bearer {auth_token}"
    })
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
                identity=str(admin.id),
                additional_claims={"role": "admin"}
            )

    res = client.get('/api/v1/pets', headers={
        "Authorization": f"Bearer {token}"
    })
    print(f"\nAcceso con rol admin: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403