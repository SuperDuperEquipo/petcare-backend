def test_smoke_get_tips(client, auth_token):
    """Humo: GET /api/v1/tips, debe devolver 200"""
    res = client.get(
        "/api/v1/tips",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nSmoke GET tips: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200


def test_smoke_post_tips(client, admin_token):
    """Humo: POST /api/v1/tips, debe devolver 201"""
    res = client.post(
        "/api/v1/tips",
        json={
            "title": "Tip humo",
            "content": "Contenido humo",
            "species": "Perro",
            "category": "Salud"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nSmoke POST tips: {res.status_code} - {res.get_json()}")
    assert res.status_code == 201


def test_smoke_get_tips_despues_de_crear(client, admin_token, auth_token):
    """Humo: Crear tip y luego GET debe reflejarlo"""
    
    client.post(
        "/api/v1/tips",
        json={
            "title": "Tip humo lista",
            "content": "Contenido humo lista",
            "species": "Gato",
            "category": "Nutrición"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    res = client.get(
        "/api/v1/tips",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    print(f"\nSmoke GET tips después de crear: {res.status_code} - total={res.get_json()['total']}")
    
    assert res.status_code == 200
    assert res.get_json()["total"] >= 1

def test_smoke_post_tips_sin_admin(client, auth_token):
    """Humo: POST sin admin debe fallar con 403"""
    res = client.post(
        "/api/v1/tips",
        json={
            "title": "Tip",
            "content": "Contenido",
            "species": "Perro",
            "category": "Salud"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    print(f"\nSmoke POST tips sin admin: {res.status_code} - {res.get_json()}")
    assert res.status_code == 403