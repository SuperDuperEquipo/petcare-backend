def test_smoke_get_appointments(client, auth_token):
    """Humo: GET /api/v1/appointments, debe devolver 200"""
    res = client.get(
        "/api/v1/appointments", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nSmoke GET appointments: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_smoke_post_appointments(client, auth_token, pet_id):
    """Humo: POST /api/v1/appointments, debe devolver 201"""
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
    print(f"\nSmoke POST appointment: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201


def test_smoke_get_appointments_por_id(client, auth_token, appointment_id):
    """Humo: GET /api/v1/appointments/:appointment_id, debe devolver 200"""
    res = client.get(
        f"/api/v1/appointments/{appointment_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke GET appointment por id: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_smoke_put_appointment(client, auth_token, appointment_id):
    """Humo: PUT /api/v1/appointments/:appointment_id, debe devolver 200"""
    res = client.put(
        f"/api/v1/appointments/{appointment_id}",
        json={"title": "Humo Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke PUT appointment: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_smoke_delete_appointment(client, auth_token, appointment_id):
    """Humo: DELETE /api/v1/appointments/:appointment_id, debe devolver 200"""
    res = client.delete(
        f"/api/v1/appointments/{appointment_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke DELETE appointment: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
