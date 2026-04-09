def test_get_users_con_admin(client, admin_token):
    """Admin puede obtener lista de usuarios"""
    res = client.get(
        '/api/v1/admin/users',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nLista users: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200
    assert 'users' in res.get_json()


def test_delete_user_flujo_completo(client, admin_token, user_id):
    """Crear usuario y luego eliminarlo"""
    
    res = client.delete(
        f'/api/v1/admin/users/{user_id}',
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    print(f"\nDelete user: {res.status_code} - {res.get_json()}")
    assert res.status_code == 200

    res_check = client.delete(
        f'/api/v1/admin/users/{user_id}',
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    print(f"\nDelete user otra vez: {res_check.status_code}")
    assert res_check.status_code == 404

def test_admin_crea_tip(client, admin_token, auth_token):
    """Admin crea tip y usuario normal lo puede ver"""

    res_create = client.post(
        "/api/v1/tips",
        json={
            "title": "Tip admin",
            "content": "Contenido admin",
            "species": "Perro",
            "category": "Salud"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    print(f"\nAdmin crea tip: {res_create.status_code}")
    assert res_create.status_code == 201

    res_get = client.get(
        "/api/v1/tips",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    data = res_get.get_json()
    print(f"\nUsuario ve tips: total={data['total']}")

    assert res_get.status_code == 200
    assert data["total"] >= 1