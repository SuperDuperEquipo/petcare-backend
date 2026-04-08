def test_smoke_get_vaccines(client, auth_token, pet_id):
    """Humo: GET /api/v1/pets/:id/vaccines debe devolver 200"""
    res = client.get(
        f"/api/v1/pets/{pet_id}/vaccines",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke GET vaccines: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200

def test_smoke_post_vaccine(client, auth_token, pet_id):
    """Humo: POST /api/v1/pets/:id/vaccines debe devolver 201"""
    res = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Rabia", "vet": "Dr. Juan", "date_applied": "2025-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke POST vaccine: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201

def test_smoke_get_vaccine_by_id(client, auth_token, pet_id):
    """Humo: GET /api/v1/vaccines/:id debe devolver 200"""
    # Primero se crea una vacuna para asegurar que existe un ID válido para la prueba 
    res_create = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Parvovirus", "vet": "Dr. Juan", "date_applied": "2025-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vaccine_id = res_create.get_json()["vacuna"]["id"]

    res = client.get(
        f"/api/v1/vaccines/{vaccine_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke GET vaccine por id: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200

def test_smoke_put_vaccine(client, auth_token, pet_id):
    """Humo: PUT /api/v1/vaccines/:id debe devolver 200"""
    res_create = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Moquillo", "vet": "Dr. Juan", "date_applied": "2025-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vaccine_id = res_create.get_json()["vacuna"]["id"]

    res = client.put(
        f"/api/v1/vaccines/{vaccine_id}",
        json={"name": "Moquillo Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke PUT vaccine: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200

def test_smoke_delete_vaccine(client, auth_token, pet_id):
    """Humo: DELETE /api/v1/vaccines/:id debe devolver 200"""
    res_create = client.post(
        f"/api/v1/pets/{pet_id}/vaccines",
        json={"name": "Hepatitis", "vet": "Dr. Roberto", "date_applied": "2025-01-01"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    vaccine_id = res_create.get_json()["vacuna"]["id"]

    res = client.delete(
        f"/api/v1/vaccines/{vaccine_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke DELETE vaccine: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200