# Pruebas unitarias
def test_get_appointments_sin_token(client):
    """Sin token debe devolver 401"""
    res = client.get("/api/v1/appointments")
    print(f"\nRespuesta sin token: {res.status_code} - {res.get_json()}")
    assert res.status_code == 401


def test_crear_appointment_sin_title(client, auth_token, pet_id):
    """Sin title debe devolver 422"""
    res = client.post(
        "/api/v1/appointments",
        json={
            "date": "2027-04-01",
            "time": "10:00:00",
            "type": "Consulta",
            "pet_id": pet_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError sin title: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422


def test_crear_appointment_sin_date(client, auth_token, pet_id):
    """Sin date debe devolver 422"""
    res = client.post(
        "/api/v1/appointments",
        json={
            "title": "Consulta",
            "time": "10:00:00",
            "type": "Consulta",
            "pet_id": pet_id,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError sin date: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422


def test_crear_appointment_sin_pet_id(client, auth_token):
    """Sin pet_id debe devolver 422"""
    res = client.post(
        "/api/v1/appointments",
        json={
            "title": "Consulta",
            "date": "2027-04-01",
            "time": "10:00:00",
            "type": "Consulta",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError sin pet_id: {res.status_code} - {res.get_json()}")
    assert res.status_code == 422


def test_crear_appointment_body_no_json(client, auth_token):
    """Body que no es JSON debe devolver 400"""
    res = client.post(
        "/api/v1/appointments",
        data="no es un JSON",
        content_type="text/plain",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nError body no JSON: {res.status_code} - {res.get_json()}")
    assert res.status_code == 400


def test_get_appointment_inexistente(client, auth_token):
    """ID que no existe debe devolver 404"""
    res = client.get(
        "/api/v1/appointments/999", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nCita no encontrada: {res.status_code} - {res.get_json()}")
    assert res.status_code == 404
