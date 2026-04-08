def test_get_appointments_con_token(client, auth_token):
    """Con token válido debe devolver lista vacía"""
    res = client.get(
        "/api/v1/appointments", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nLista de citas: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()["total"] == 0


def test_crear_appointment_exitoso(client, auth_token, pet_id):
    """Crear cita con datos válidos"""
    res = client.post(
        "/api/v1/appointments",
        json={
            "title": "Consulta general",
            "date": "2027-04-01",
            "time": "10:00:00",
            "type": "Consulta",
            "pet_id": pet_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nCita creada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201
    assert res.get_json()["cita"]["titulo"] == "Consulta general"


def test_get_appointment_por_id(client, auth_token, appointment_id):
    """Obtener cita por ID existente"""
    res = client.get(
        f"/api/v1/appointments/{appointment_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nCita por id: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()["cita"]["id"] == appointment_id


def test_actualizar_appointment(client, auth_token, appointment_id):
    """Actualizar una cita existente"""
    res = client.put(
        f"/api/v1/appointments/{appointment_id}",
        json={"title": "Consulta actualizada"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nCita actualizada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert res.get_json()["cita"]["titulo"] == "Consulta actualizada"


def test_eliminar_appointment(client, auth_token, appointment_id):
    """Eliminar una cita existente"""
    res = client.delete(
        f"/api/v1/appointments/{appointment_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nCita eliminada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_crear_appointment_y_verificar_en_lista(client, auth_token, pet_id):
    """Crear cita y verificar que aparece en el GET"""
    client.post(
        "/api/v1/appointments",
        json={
            "title": "Vacuna anual",
            "date": "2027-05-01",
            "time": "09:00:00",
            "type": "Vacuna",
            "pet_id": pet_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    res = client.get(
        "/api/v1/appointments", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nCita en lista: {res.status_code} - total={res.get_json()['total']}")
    assert res.status_code == 200
    assert res.get_json()["total"] == 1


def test_crear_appointment_mascota_ajena(client, auth_token, app):
    """Crear cita con mascota de otro usuario debe devolver 404"""
    from app.core.extensions import db
    from app.auth.models.user import User
    from app.pets.models.pet import Pet

    with app.app_context():
        otro_user = User(name="Otro", email="otro@petcare.com", role="user")
        otro_user.set_password("123456")
        db.session.add(otro_user)
        db.session.commit()

        mascota_ajena = Pet(name="Ajena", species="Gato", user_id=otro_user.id)
        db.session.add(mascota_ajena)
        db.session.commit()
        mascota_ajena_id = mascota_ajena.id

    res = client.post(
        "/api/v1/appointments",
        json={
            "title": "Consulta",
            "date": "2027-04-01",
            "time": "10:00:00",
            "type": "Consulta",
            "pet_id": mascota_ajena_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nCita con mascota ajena: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404


def test_crear_appointment_rol_admin(client, admin_token):
    """Un admin no puede crear citas, debe devolver 403"""
    res = client.post(
        "/api/v1/appointments",
        json={
            "title": "Consulta",
            "date": "2027-04-01",
            "time": "10:00:00",
            "type": "Consulta",
            "pet_id": 1,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    print(f"\nError rol admin: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403
