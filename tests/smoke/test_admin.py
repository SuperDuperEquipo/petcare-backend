def test_smoke_get_users(client, admin_token):
    """Humo: GET users debe devolver 200"""
    res = client.get(
        '/api/v1/admin/users',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nSmoke GET users: {res.status_code}")
    assert res.status_code == 200


def test_smoke_delete_user(client, admin_token, user_id):
    """Humo: DELETE user debe devolver 200"""
    res = client.delete(
        f'/api/v1/admin/users/{user_id}',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nSmoke DELETE user: {res.status_code}")
    assert res.status_code == 200

def test_smoke_delete_user_no_existente(client, admin_token):
    """Humo: DELETE user inexistente debe devolver 404"""
    res = client.delete(
        '/api/v1/admin/users/9999',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    print(f"\nSmoke DELETE inexistente: {res.status_code}")
    assert res.status_code == 404