def test_smoke_get_pets(client, auth_token):
    """Humo: GET /api/v1/pets, debe devolver 200"""
    res = client.get("/api/v1/pets", headers={"Authorization": f"Bearer {auth_token}"})
    print(f"\nSmoke GET pets: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_smoke_post_pets(client, auth_token):
    """Humo: POST /api/v1/pets, debe devolver 201"""
    res = client.post(
        "/api/v1/pets",
        json={"name": "Humo", "species": "Perro"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke POST pets: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201


def test_smoke_get_pet_por_id(client, auth_token, pet_id):
    """Humo: GET /api/v1/pets/:id, debe devolver 200"""
    res = client.get(
        f"/api/v1/pets/{pet_id}", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nSmoke GET pet por id: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_smoke_put_pet(client, auth_token, pet_id):
    """Humo: PUT /api/v1/pets/:id, debe devolver 200"""
    res = client.put(
        f"/api/v1/pets/{pet_id}",
        json={"name": "Humo Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    print(f"\nSmoke PUT pet: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_smoke_delete_pet(client, auth_token, pet_id):
    """Humo: DELETE /api/v1/pets/:id, debe devolver 200"""
    res = client.delete(
        f"/api/v1/pets/{pet_id}", headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nSmoke DELETE pet: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
